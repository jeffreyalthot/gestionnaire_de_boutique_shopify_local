from customer_service.ticket_router import TicketRouter

def test_ticket_router_maps_operational_queues():
    router=TicketRouter()
    assert router.route("chargeback")=="finance" and router.route("lost_package")=="fulfillment" and router.route("other")=="customer_service"
