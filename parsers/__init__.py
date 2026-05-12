"""Parsers package."""

from .work_ua import WorkUaListingParser, WorkUaResumeParser, parse_work_ua_listings, parse_work_ua_resume
from .robota_ua import RobotaUaListingParser, RobotaUaResumeParser, parse_robota_ua_listings, parse_robota_ua_resume

__all__ = [
    "WorkUaListingParser",
    "WorkUaResumeParser",
    "parse_work_ua_listings",
    "parse_work_ua_resume",
    "RobotaUaListingParser",
    "RobotaUaResumeParser",
    "parse_robota_ua_listings",
    "parse_robota_ua_resume",
]