from services.presentation.utilities.timer import LessonTimer
from services.presentation.utilities.countdown import Countdown
from services.presentation.utilities.breaks import BreakReminder
from services.presentation.utilities.attendance import AttendanceTracker
from services.presentation.utilities.statistics import PresentationStatistics, AnalyticsManager

class UtilityManager:
    def __init__(self) -> None:
        self.timer = LessonTimer()
        self.countdown = Countdown()
        self.breaks = BreakReminder()
        self.attendance = AttendanceTracker()
        self.statistics = PresentationStatistics()
