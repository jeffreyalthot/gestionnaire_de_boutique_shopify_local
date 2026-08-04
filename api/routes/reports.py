from fastapi import APIRouter,HTTPException
from reports.operational_summary_report import OperationalSummaryReport
from reports.report_registry import ReportRegistry
from reports.catalog_quality_report import CatalogQualityReport
from reports.cashflow_report import CashflowReport
from reports.customer_service_report import CustomerServiceReport
from reports.order_exception_report import OrderExceptionReport
from reports.supplier_performance_report import SupplierPerformanceReport

def router_for(container):
    router=APIRouter(prefix="/reports",tags=["reports"]);registry=ReportRegistry()
    for name,factory in (("operational",OperationalSummaryReport),("catalog_quality",CatalogQualityReport),("cashflow",CashflowReport),("customer_service",CustomerServiceReport),("order_exceptions",OrderExceptionReport),("supplier_performance",SupplierPerformanceReport)):registry.register(name,factory)
    @router.get("")
    async def names():return {"reports":registry.names()}
    @router.get("/{name}")
    async def report(name: str):
        if name not in registry.names():raise HTTPException(404,"rapport inconnu")
        return registry.generate(name,container.db)
    return router
