import asyncpg
import os
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        if not DATABASE_URL:
            print("DATABASE_URL not found, using JSON fallback")
            return False
        try:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
            await self.create_tables()
            print("Database connected successfully")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    async def close(self):
        if self.pool:
            await self.pool.close()
    
    async def create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS guild_config (
                    guild_id BIGINT PRIMARY KEY,
                    log_channel_id BIGINT,
                    notification_channel_id BIGINT,
                    notifications_enabled BOOLEAN DEFAULT FALSE,
                    remove_previous_rewards BOOLEAN DEFAULT FALSE,
                    update_each_message BOOLEAN DEFAULT TRUE,
                    welcome_channel_id BIGINT,
                    excluded_channels TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS role_rewards (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    level INTEGER NOT NULL,
                    role_id BIGINT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(guild_id, level)
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS user_levels_cache (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    level INTEGER DEFAULT 0,
                    xp INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT NOW(),
                    UNIQUE(guild_id, user_id)
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS role_logs (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    role_id BIGINT NOT NULL,
                    action VARCHAR(10) NOT NULL,
                    level INTEGER,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS level_notifications (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    old_level INTEGER,
                    new_level INTEGER NOT NULL,
                    notified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
    
    async def get_guild_config(self, guild_id: int):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM guild_config WHERE guild_id = $1',
                guild_id
            )
            return dict(row) if row else None
    
    async def set_guild_config(self, guild_id: int, **kwargs):
        async with self.pool.acquire() as conn:
            existing = await self.get_guild_config(guild_id)
            if existing:
                set_clause = ', '.join([f"{k} = ${i+2}" for i, k in enumerate(kwargs.keys())])
                query = f'UPDATE guild_config SET {set_clause}, updated_at = NOW() WHERE guild_id = $1'
                await conn.execute(query, guild_id, *kwargs.values())
            else:
                columns = ['guild_id'] + list(kwargs.keys())
                placeholders = ', '.join([f'${i+1}' for i in range(len(columns))])
                query = f'INSERT INTO guild_config ({", ".join(columns)}) VALUES ({placeholders})'
                await conn.execute(query, guild_id, *kwargs.values())
    
    async def get_role_rewards(self, guild_id: int):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                'SELECT * FROM role_rewards WHERE guild_id = $1 ORDER BY level ASC',
                guild_id
            )
            return [dict(row) for row in rows]
    
    async def add_role_reward(self, guild_id: int, level: int, role_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO role_rewards (guild_id, level, role_id)
                VALUES ($1, $2, $3)
                ON CONFLICT (guild_id, level) DO UPDATE SET role_id = $3
            ''', guild_id, level, role_id)
    
    async def remove_role_reward(self, guild_id: int, level: int):
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                'DELETE FROM role_rewards WHERE guild_id = $1 AND level = $2',
                guild_id, level
            )
            return 'DELETE 1' in result
    
    async def get_cached_level(self, guild_id: int, user_id: int):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM user_levels_cache WHERE guild_id = $1 AND user_id = $2',
                guild_id, user_id
            )
            return dict(row) if row else None
    
    async def update_cached_level(self, guild_id: int, user_id: int, level: int, xp: int = 0):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO user_levels_cache (guild_id, user_id, level, xp, last_updated)
                VALUES ($1, $2, $3, $4, NOW())
                ON CONFLICT (guild_id, user_id) DO UPDATE SET 
                    level = $3, xp = $4, last_updated = NOW()
            ''', guild_id, user_id, level, xp)
    
    async def log_role_action(self, guild_id: int, user_id: int, role_id: int, action: str, level: int = None):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO role_logs (guild_id, user_id, role_id, action, level)
                VALUES ($1, $2, $3, $4, $5)
            ''', guild_id, user_id, role_id, action, level)
    
    async def get_role_logs(self, guild_id: int, limit: int = 50):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                'SELECT * FROM role_logs WHERE guild_id = $1 ORDER BY created_at DESC LIMIT $2',
                guild_id, limit
            )
            return [dict(row) for row in rows]
    
    async def get_guild_stats(self, guild_id: int):
        async with self.pool.acquire() as conn:
            total_rewards = await conn.fetchval(
                'SELECT COUNT(*) FROM role_rewards WHERE guild_id = $1',
                guild_id
            )
            total_logs = await conn.fetchval(
                'SELECT COUNT(*) FROM role_logs WHERE guild_id = $1',
                guild_id
            )
            cached_users = await conn.fetchval(
                'SELECT COUNT(*) FROM user_levels_cache WHERE guild_id = $1',
                guild_id
            )
            level_distribution = await conn.fetch('''
                SELECT level, COUNT(*) as count 
                FROM user_levels_cache 
                WHERE guild_id = $1 
                GROUP BY level 
                ORDER BY level DESC
                LIMIT 10
            ''', guild_id)
            
            return {
                'total_rewards': total_rewards,
                'total_logs': total_logs,
                'cached_users': cached_users,
                'level_distribution': [dict(row) for row in level_distribution]
            }
    
    async def export_config(self, guild_id: int):
        config = await self.get_guild_config(guild_id)
        rewards = await self.get_role_rewards(guild_id)
        return {
            'config': config,
            'rewards': rewards,
            'exported_at': datetime.now().isoformat()
        }
    
    async def import_config(self, guild_id: int, data: dict):
        if 'config' in data and data['config']:
            config = data['config']
            config.pop('guild_id', None)
            config.pop('created_at', None)
            config.pop('updated_at', None)
            await self.set_guild_config(guild_id, **config)
        
        if 'rewards' in data:
            async with self.pool.acquire() as conn:
                await conn.execute('DELETE FROM role_rewards WHERE guild_id = $1', guild_id)
            for reward in data['rewards']:
                await self.add_role_reward(guild_id, reward['level'], reward['role_id'])

db = Database()
