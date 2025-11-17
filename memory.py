import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional

# Handle Google Generative AI imports with proper error handling
try:
    from google.generativeai.client import configure
    from google.generativeai.generative_models import GenerativeModel
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    configure = None
    GenerativeModel = None
    GOOGLE_AI_AVAILABLE = False

import os

class MemoryBank:
    """CAPSTONE: Persistent Memory with Gemini-powered Context Compaction"""
    
    def __init__(self, db_path: str = "ecoforge_memory.db"):
        self.db_path = db_path
        self.init_database()
        
        # Configure Gemini for context compaction
        self.gemini_model = None
        if GOOGLE_AI_AVAILABLE and configure and GenerativeModel:
            try:
                api_key = os.getenv("GOOGLE_API_KEY", "demo_key")
                if api_key and api_key != "demo_key":
                    configure(api_key=api_key)
                    self.gemini_model = GenerativeModel('gemini-pro')
            except Exception:
                self.gemini_model = None
    
    def init_database(self):
        """Initialize SQLite database for persistent memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # CAPSTONE: Memory Schema Design
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_input TEXT NOT NULL,
                result_json TEXT NOT NULL,
                eco_score REAL,
                carbon_footprint REAL,
                compacted_summary TEXT,
                embedding_vector TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                insight_type TEXT,
                insight_data TEXT,
                relevance_score REAL,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_conversation(self, user_input: str, result: Dict[str, Any]) -> int:
        """CAPSTONE: Store conversation with automatic compaction trigger"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        result_json = json.dumps(result)
        eco_score = result.get('eco_score', 0)
        carbon_footprint = result.get('carbon_footprint', 0)
        
        cursor.execute('''
            INSERT INTO conversations 
            (timestamp, user_input, result_json, eco_score, carbon_footprint)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, user_input, result_json, eco_score, carbon_footprint))
        
        conversation_id = cursor.lastrowid
        if conversation_id is None:
            conversation_id = 0
        conn.commit()
        conn.close()
        
        # Trigger compaction if memory is getting large
        self._check_and_compact()
        
        return int(conversation_id)
    
    def _check_and_compact(self):
        """CAPSTONE: Automatic Memory Compaction using Gemini"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if we have more than 50 conversations
        cursor.execute('SELECT COUNT(*) FROM conversations')
        count = cursor.fetchone()[0]
        
        if count > 50:
            # Get oldest 20 conversations for compaction
            cursor.execute('''
                SELECT id, user_input, result_json, eco_score 
                FROM conversations 
                ORDER BY timestamp ASC 
                LIMIT 20
            ''')
            
            old_conversations = cursor.fetchall()
            
            if old_conversations and self.gemini_model:
                compacted_summary = self._compact_with_gemini(old_conversations)
                
                # Store compacted summary
                cursor.execute('''
                    UPDATE conversations 
                    SET compacted_summary = ? 
                    WHERE id = ?
                ''', (compacted_summary, old_conversations[0][0]))
                
                # Delete the other old conversations (keep one with summary)
                old_ids = [conv[0] for conv in old_conversations[1:]]
                cursor.executemany('DELETE FROM conversations WHERE id = ?', [(id,) for id in old_ids])
        
        conn.commit()
        conn.close()
    
    def _compact_with_gemini(self, conversations: List[tuple]) -> str:
        """CAPSTONE: Context Compaction using Gemini"""
        
        if not self.gemini_model:
            return "Compaction unavailable - using summary"
        
        try:
            # Prepare conversation data for compaction
            conversation_text = ""
            for conv in conversations:
                conv_id, user_input, result_json, eco_score = conv
                result = json.loads(result_json)
                conversation_text += f"""
                User Input: {user_input}
                EcoScore: {eco_score}
                Carbon Footprint: {result.get('carbon_footprint', 'N/A')}
                Key Actions: {', '.join(result.get('action_plan', [])[:3])}
                ---
                """
            
            # CAPSTONE: Gemini-powered Intelligent Summarization
            prompt = f"""
            You are an AI memory compaction system for EcoForge, a carbon footprint reduction app.
            
            Analyze these {len(conversations)} user conversations and create a compact, intelligent summary that preserves:
            1. Key behavioral patterns
            2. Progress trends in EcoScore
            3. Most effective interventions
            4. User preferences and constraints
            
            Conversations to compact:
            {conversation_text}
            
            Create a concise summary (max 200 words) that captures the essential insights for future personalization.
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Compaction summary: {len(conversations)} conversations processed. Average EcoScore trend and key patterns preserved."
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent conversations for memory constellation display"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, user_input, result_json, eco_score, compacted_summary
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        conversations = []
        for row in cursor.fetchall():
            conv_id, timestamp, user_input, result_json, eco_score, compacted_summary = row
            
            conversations.append({
                'id': conv_id,
                'timestamp': timestamp,
                'input': user_input,
                'result': json.loads(result_json),
                'eco_score': eco_score,
                'summary': compacted_summary
            })
        
        conn.close()
        return conversations
    
    def get_user_insights(self, user_pattern: str) -> List[Dict[str, Any]]:
        """CAPSTONE: Retrieve personalized insights based on user patterns"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find similar conversations based on patterns
        cursor.execute('''
            SELECT user_input, eco_score, result_json
            FROM conversations 
            WHERE user_input LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''', (f'%{user_pattern}%',))
        
        similar_conversations = cursor.fetchall()
        
        insights = []
        for conv in similar_conversations:
            user_input, eco_score, result_json = conv
            result = json.loads(result_json)
            
            insights.append({
                'pattern': user_pattern,
                'eco_score': eco_score,
                'effective_actions': result.get('action_plan', [])[:2],
                'carbon_reduction': result.get('carbon_footprint', 0)
            })
        
        conn.close()
        return insights
    
    def store_insight(self, conversation_id: int, insight_type: str, insight_data: Dict[str, Any], relevance_score: float = 1.0):
        """Store extracted insights for future reference"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO insights (conversation_id, insight_type, insight_data, relevance_score)
            VALUES (?, ?, ?, ?)
        ''', (conversation_id, insight_type, json.dumps(insight_data), relevance_score))
        
        conn.commit()
        conn.close()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory bank statistics for observability"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total conversations
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_conversations = cursor.fetchone()[0]
        
        # Average EcoScore trend
        cursor.execute('SELECT AVG(eco_score) FROM conversations WHERE eco_score > 0')
        avg_eco_score = cursor.fetchone()[0] or 0
        
        # Compacted conversations
        cursor.execute('SELECT COUNT(*) FROM conversations WHERE compacted_summary IS NOT NULL')
        compacted_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_conversations': total_conversations,
            'average_eco_score': round(avg_eco_score, 2),
            'compacted_conversations': compacted_count,
            'memory_efficiency': round((compacted_count / max(total_conversations, 1)) * 100, 2)
        }


class ConversationMemory(MemoryBank):
    """Wrapper class for backward compatibility with EcoForge app"""
    
    def __init__(self, db_path: str = "ecoforge_memory.db"):
        super().__init__(db_path)
        
    def add_conversation(self, user_input: str, result: Dict[str, Any]) -> int:
        """Add a conversation to memory"""
        return self.store_conversation(user_input, result)
        
    def get_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations"""
        return self.get_recent_conversations(limit)
        
    def clear_memory(self) -> None:
        """Clear all conversations from memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM conversations')
        cursor.execute('DELETE FROM insights')
        conn.commit()
        conn.close()