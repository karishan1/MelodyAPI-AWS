from app.utils.dynamodb_cache import convert_floats_to_decimal, generate_fingerprint, store_fingerprint,get_fingerprint; 
from decimal import Decimal;
from unittest.mock import patch, MagicMock


def test_convert_floats_to_decimal():

    input_data = {
        "a": 0.5,
        "b": [1.1, 2.2],
        "c": {"d": 3.3}
    }
    result = convert_floats_to_decimal(input_data)
    assert result["a"] == Decimal("0.5")
    assert result["b"] == [Decimal("1.1"), Decimal("2.2")]
    assert result["c"]["d"] == Decimal("3.3")

###### Fingerprint Generation ######
@patch("app.utils.dynamodb_cache.subprocess.run")
def test_generate_fingerprint_success(mock_run):
    mock_run.return_value.stdout = '{"fingerprint": "abc123"}'
    result = generate_fingerprint("fake_audio.mp3")
    assert result == "abc123"

@patch("app.utils.dynamodb_cache.subprocess.run")
def test_generate_fingerprint_failure(mock_run):
    mock_run.side_effect = Exception("Simulated fpcalc error")
    result = generate_fingerprint("invalid_audio.mp3")
    assert result is None


###### Store Fingerprint ######
@patch("app.utils.dynamodb_cache.dynamodb")
def test_store_fingerprint(mock_dynamodb):
    mock_table = MagicMock() # Uses mock table 
    mock_dynamodb.Table.return_value = mock_table 
    result = store_fingerprint(
        fingerprint="abc123",
        category="genre",
        classification={"rock": 0.9},
        predictions_num=1,
        ttl_seconds=10
    )
    assert result == {"message": "Fingerprint Stored Successfully"}
    mock_table.put_item.assert_called_once() # Ensures put item was called once 

    item = mock_table.put_item.call_args[1]["Item"] # Checks stored value
    assert item["fingerprint"] == "abc123_genre_1"
    assert item["category"] == "genre"

##### Fingerprint retrieval #####
@patch("app.utils.dynamodb_cache.dynamodb")
def test_get_fingerprint_success(mock_dynamodb):
    mock_table = MagicMock()
    mock_dynamodb.Table.return_value = mock_table 

    mock_table.get_item.return_value = {
        "Item": {
            "fingerprint": "abc123_genre_1",
            "category": "genre",
            "classification": {"rock": 0.9},
            "predictions_num": 1,
            "ttl": 10
        }
    }

    result = get_fingerprint("abc123","genre",1)
    assert result["fingerprint"] == "abc123_genre_1"
    assert result["category"] == "genre"
    assert result["classification"]["rock"] == 0.9

@patch("app.utils.dynamodb_cache.dynamodb")
def test_get_fingerprint_not_found(mock_dynamodb):
    mock_table = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_table.get_item.return_value = {} 
    result = get_fingerprint("abc123","genre",1)

    assert result is None


