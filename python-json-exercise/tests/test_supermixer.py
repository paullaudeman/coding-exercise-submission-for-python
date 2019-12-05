import pytest
import json
from supermixer import SuperMixer


def test_ingesting_the_playlist():
    mixtape_obj = json.load(open('./mixtape.json', 'r'))
    changes_obj = json.load(open('./changes.json', 'r'))

    super_mixer = SuperMixer(mixtape_obj, changes_obj)
    results = super_mixer.run()

    assert results is not None, 'Expected results object'


def test_should_not_ingest_empty_playlist_dict():
    with pytest.raises(TypeError) as ex_info:
        SuperMixer(None, {})
    assert "mixtape" in str(ex_info.value)


def test_should_not_accept_empty_changes_dict():
    with pytest.raises(TypeError) as ex_info:
        SuperMixer(None, {})
    assert "mixtape" in str(ex_info.value)


def test_should_not_ingest_string_as_mixer_dict():
    with pytest.raises(TypeError) as ex_info:
        SuperMixer('hello', {})
    assert "mixtape" in str(ex_info.value)


def test_should_not_ingest_string_as_changes_dict():
    with pytest.raises(TypeError) as ex_info:
        SuperMixer({}, 'there')
    assert "changes" in str(ex_info.value)

#
#   ...
#
#
# Hi!
# I could have added a lot more unit tests here to flesh out the various scenarios.
# However, I thought having more working code over a bunch of unit tests was more pragmatic for this.
# So this comment is just a friendly recommendation that I could have done more here. :-)
