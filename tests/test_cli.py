from road_traffic import __main__


def test_cli_main_runs(monkeypatch):
    called = {"ok": False}

    def fake_run():
        called["ok"] = True

    monkeypatch.setattr(__main__, "run", fake_run)

    __main__.main()

    assert called["ok"] is True
