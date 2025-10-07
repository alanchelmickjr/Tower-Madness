"""
Leaderboard management system for Tower Madness
Handles persistent high scores and session tracking
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class LeaderboardManager:
    """Manages game leaderboard with persistent storage and session tracking."""
    
    def __init__(self, filename: str = "highscores.json", max_scores: int = 10):
        """Initialize the leaderboard manager.
        
        Args:
            filename: Path to the JSON file for storing scores
            max_scores: Maximum number of scores to keep in all-time leaderboard
        """
        self.filename = filename
        self.max_scores = max_scores
        self.all_time_scores: List[Dict] = []
        self.session_scores: List[Dict] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load existing scores
        self.load_scores()
        
    def load_scores(self) -> bool:
        """Load scores from JSON file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.all_time_scores = data.get('all_time', [])
                    # Ensure scores are sorted
                    self.all_time_scores.sort(key=lambda x: x['score'], reverse=True)
                    return True
            else:
                # Create empty leaderboard
                self.all_time_scores = []
                self.save_scores()
                return True
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            self.all_time_scores = []
            return False
            
    def save_scores(self) -> bool:
        """Save scores to JSON file.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            data = {
                'all_time': self.all_time_scores[:self.max_scores],
                'version': '1.0',
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
            return False
            
    def add_score(self, name: str, score: int, passengers_delivered: int = 0) -> Dict:
        """Add a new score to both all-time and session leaderboards.
        
        Args:
            name: Player name (3 characters)
            score: Final score
            passengers_delivered: Number of passengers delivered
            
        Returns:
            Dictionary with score entry and rank information
        """
        entry = {
            'name': name.upper()[:3],  # Ensure 3 characters, uppercase
            'score': score,
            'passengers': passengers_delivered,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'session_id': self.session_id
        }
        
        # Add to session scores
        self.session_scores.append(entry)
        self.session_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Add to all-time scores
        self.all_time_scores.append(entry)
        self.all_time_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top scores
        self.all_time_scores = self.all_time_scores[:self.max_scores]
        
        # Save to file
        self.save_scores()
        
        # Calculate ranks
        all_time_rank = self._get_rank(entry, self.all_time_scores)
        session_rank = self._get_rank(entry, self.session_scores)
        
        return {
            'entry': entry,
            'all_time_rank': all_time_rank,
            'session_rank': session_rank,
            'is_all_time_high': all_time_rank == 1,
            'is_session_high': session_rank == 1,
            'made_all_time_board': all_time_rank <= self.max_scores
        }
        
    def _get_rank(self, entry: Dict, score_list: List[Dict]) -> int:
        """Get the rank of an entry in a score list.
        
        Args:
            entry: Score entry to find
            score_list: List of scores to search
            
        Returns:
            Rank (1-based), or -1 if not found
        """
        try:
            return score_list.index(entry) + 1
        except ValueError:
            return -1
            
    def is_high_score(self, score: int) -> bool:
        """Check if a score qualifies for the all-time leaderboard.
        
        Args:
            score: Score to check
            
        Returns:
            True if score makes the top 10, False otherwise
        """
        if len(self.all_time_scores) < self.max_scores:
            return True
        return score > self.all_time_scores[-1]['score']
        
    def get_top_scores(self, n: int = 10) -> List[Dict]:
        """Get top N all-time scores.
        
        Args:
            n: Number of scores to return
            
        Returns:
            List of score dictionaries
        """
        return self.all_time_scores[:n]
        
    def get_session_scores(self, n: int = 5) -> List[Dict]:
        """Get top N session scores.
        
        Args:
            n: Number of scores to return
            
        Returns:
            List of score dictionaries
        """
        return self.session_scores[:n]
        
    def clear_session(self):
        """Clear session scores and start a new session."""
        self.session_scores = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def get_high_score(self) -> int:
        """Get the current high score.
        
        Returns:
            Highest score, or 0 if no scores exist
        """
        if self.all_time_scores:
            return self.all_time_scores[0]['score']
        return 0
        
    def get_session_high_score(self) -> int:
        """Get the current session high score.
        
        Returns:
            Highest session score, or 0 if no scores exist
        """
        if self.session_scores:
            return self.session_scores[0]['score']
        return 0