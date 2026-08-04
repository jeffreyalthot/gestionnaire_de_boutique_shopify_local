from store_management.store_settings_sync import StoreSettingsSync

def test_store_settings_sync_only_emits_safe_differences():
    changes=StoreSettingsSync().diff({"currency":"CAD","secret":"x"},{"currency":"USD","secret":"y"})
    assert changes=={"currency":{"local":"CAD","remote":"USD"}}
