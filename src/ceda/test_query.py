from cdsetool.query import query_features, shape_to_wkt
from cdsetool.credentials import Credentials
from cdsetool.download import download_features
from cdsetool.monitor import StatusMonitor
from datetime import date

features = query_features(
    "SENTINEL-1",
    {
        "contentDateStartGe": "2026-09-10",
        "contentDateStartLe": date(2026, 9, 10),
        "processingLevel": "LEVEL1",
        "productType": "IW_GRDH_1S",
    },
)

list(
    download_features(
        features,
        "C:\\Users\\sjdd53\\Downloads",
        {
            "concurrency": 4,
            "monitor": StatusMonitor(),
            "credentials": Credentials("steve.donegan@stfc.ac.uk", "8MKZVzJFp7gGRvX2Yppw!"),
        },
    )
)

print ('here')