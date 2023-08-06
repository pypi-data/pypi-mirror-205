from .wcs import WcsServiceNode, WcsNodeOperationGetCoverage, WcsNodeOperationDescribeCoverage, \
    WcsGetCoveragePredicate, WcsDescribeCoveragePredicate, WcsFactory
from . import _version

__version__ = _version.get_versions()['version']
__all__ = [
    'WcsServiceNode',
    'WcsNodeOperationGetCoverage',
    'WcsNodeOperationDescribeCoverage',
    'WcsGetCoveragePredicate',
    'WcsDescribeCoveragePredicate',
    'WcsFactory'
]



