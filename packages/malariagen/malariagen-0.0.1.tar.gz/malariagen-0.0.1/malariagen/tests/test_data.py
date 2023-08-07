from packaging.version import Version, parse
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

import malariagen.data
from malariagen.data import Af1, Ag3


def test_version():
    assert hasattr(malariagen.data, "__version__")
    assert isinstance(malariagen.data.__version__, str)
    version = parse(malariagen.data.__version__)
    assert isinstance(version, Version)


def setup_subclass(subclass, url=None, **kwargs):
    kwargs.setdefault("check_location", False)
    kwargs.setdefault("show_progress", False)
    if url is None:
        # test default URL
        return subclass(**kwargs)
    if url.startswith("simplecache::"):
        # configure the directory on the local file system to cache data
        kwargs["simplecache"] = dict(cache_storage="gcs_cache")
    return subclass(url=url, **kwargs)

@pytest.mark.parametrize(
    "subclass,url,release,sample_sets_count",
    [
        (Ag3, None, "3.0", 28),
        (Ag3, "gs://vo_agam_release", "3.0", 28),
        (Ag3, "gcs://vo_agam_release", "3.0", 28),
        (Ag3, "simplecache::gs://vo_agam_release/", "3.0", 28),
        (Ag3, "simplecache::gcs://vo_agam_release/", "3.0", 28),
        (Af1, None, "1.0", 8),
        (Af1, "gs://vo_afun_release", "1.0", 8),
        (Af1, "gcs://vo_afun_release", "1.0", 8),
        (Af1, "simplecache::gs://vo_afun_release/", "1.0", 8),
        (Af1, "simplecache::gcs://vo_afun_release/", "1.0", 8),
    ],
)
def test_sample_sets(subclass, url, release, sample_sets_count):
    anoph = setup_subclass(subclass, url)
    df_sample_sets = anoph.sample_sets(release=release)
    assert isinstance(df_sample_sets, pd.DataFrame)
    assert len(df_sample_sets) == sample_sets_count
    assert tuple(df_sample_sets.columns) == ("sample_set", "sample_count", "release")

    # test duplicates are handled
    df_dup = anoph.sample_sets(release=[release, release])
    assert_frame_equal(df_sample_sets, df_dup)

    # test default is all public releases
    df_default = anoph.sample_sets()
    df_all = anoph.sample_sets(release=anoph.releases)
    assert_frame_equal(df_default, df_all)
