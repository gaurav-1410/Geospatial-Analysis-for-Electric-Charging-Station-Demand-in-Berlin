import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.Application.feedback import FeedbackService

@pytest.fixture
def feedback_service() -> FeedbackService:
    """
    Fixture to provide a FeedbackService instance.

    :return: FeedbackService instance
    """
    return FeedbackService()

def test_add_feedback(feedback_service: FeedbackService) -> None:
    """
    Test that feedback is added correctly to both station and user.
    
    :param feedback_service: Instance of FeedbackService to add feedback.
    :return: None
    """
    feedback_service.add_feedback("10115", "user123", "John Doe", 5, "Excellent station!")
    assert "10115" in feedback_service.feedbacks_by_station, "Feedback was not added to the correct station"
    assert "user123" in feedback_service.feedbacks_by_user, "Feedback was not added to the correct user"

def test_get_feedbacks_for_station(feedback_service: FeedbackService) -> None:
    """
    Test that feedback can be retrieved correctly for a station.
    
    :param feedback_service: Instance of FeedbackService to fetch feedback.
    :return: None
    """
    feedback_service.add_feedback("10115", "user123", "John Doe", 4, "Good station.")
    feedbacks = feedback_service.get_feedbacks_for_station("10115")
    assert len(feedbacks) == 1, "Feedback count mismatch for station"

def test_get_feedbacks_by_user(feedback_service: FeedbackService) -> None:
    """
    Test that feedback can be retrieved correctly for a user.
    
    :param feedback_service: Instance of FeedbackService to fetch feedback.
    :return: None
    """
    feedback_service.add_feedback("10115", "user123", "John Doe", 5, "Great station!")
    feedbacks = feedback_service.get_feedbacks_by_user("user123")
    assert len(feedbacks) == 1, "Feedback count mismatch for user"
