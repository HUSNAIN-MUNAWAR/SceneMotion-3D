from vision_core.artifacts.bundle_exporter import create_artifact_bundle


def test_artifact_bundle(tmp_path):
    (tmp_path/'metrics.json').write_text('{"ok": true}', encoding='utf-8')
    z = create_artifact_bundle(tmp_path)
    assert z.endswith('.zip')
    assert (tmp_path/'artifact_bundle.zip').exists()
