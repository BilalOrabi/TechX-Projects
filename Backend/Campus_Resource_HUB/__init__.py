"""
Campus Resource Hub - A mini application coordinating students, mentors,
learning resources, and financial accounts for a fictional bootcamp.
"""

from core import (
    Wallet,
    Person,
    Student,
    PremiumStudent,
    Mentor,
    Course,
    Resource,
    ResourceStatus
)
from mixins import AuditMixin
from catalog import ResourceCatalog
from reports import Report

__version__ = "1.0.0"
__all__ = [
    'Wallet',
    'Person',
    'Student',
    'PremiumStudent',
    'Mentor',
    'Course',
    'Resource',
    'ResourceStatus',
    'AuditMixin',
    'ResourceCatalog',
    'Report',
]
