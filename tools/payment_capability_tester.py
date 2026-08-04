from app.bootstrap import bootstrap
def run() -> dict[str,object]:
    app=bootstrap()
    return {"dry_run":app.settings.app_dry_run,"alibaba_ready":app.settings.live_alibaba_ready,
            "payment_ready":app.settings.live_payment_ready,"manual_approval":app.settings.alibaba_require_manual_payment_approval}
if __name__=="__main__": print(run())
