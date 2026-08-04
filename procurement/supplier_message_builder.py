from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class SupplierInstruction:
    code: str
    text: str
    required: bool = True


class SupplierMessageBuilder:
    def build(
        self,
        *,
        order_reference: str,
        no_invoice: bool = True,
        tracking_required: bool = True,
        recipient_language: str = "en",
        fragile: bool = False,
        gift: bool = False,
        custom_instructions: Iterable[str] = (),
    ) -> str:
        reference = str(order_reference).strip()
        if not reference:
            raise ValueError("order_reference requis")
        instructions = list(self.instructions(
            order_reference=reference,
            no_invoice=no_invoice,
            tracking_required=tracking_required,
            fragile=fragile,
            gift=gift,
            custom_instructions=custom_instructions,
        ))
        prefix = "Supplier instructions" if recipient_language.lower().startswith("en") else "Instructions fournisseur"
        return prefix + ": " + " ".join(item.text for item in instructions)

    def instructions(
        self,
        *,
        order_reference: str,
        no_invoice: bool = True,
        tracking_required: bool = True,
        fragile: bool = False,
        gift: bool = False,
        custom_instructions: Iterable[str] = (),
    ) -> tuple[SupplierInstruction, ...]:
        items = [
            SupplierInstruction("reference", f"Order reference: {order_reference}."),
            SupplierInstruction("dropship", "Ship directly to the recipient using the supplied address."),
        ]
        if no_invoice:
            items.append(SupplierInstruction("blind_shipping", "Do not include supplier pricing, invoices or promotional material."))
        if tracking_required:
            items.append(SupplierInstruction("tracking", "Provide a valid trackable shipment number immediately after dispatch."))
        if fragile:
            items.append(SupplierInstruction("fragile", "Use protective packaging suitable for fragile goods."))
        if gift:
            items.append(SupplierInstruction("gift", "Do not show prices on the packing slip."))
        for index, text in enumerate(custom_instructions):
            clean = " ".join(str(text).split())
            if clean:
                items.append(SupplierInstruction(f"custom_{index + 1}", clean + ("" if clean.endswith(".") else "."), False))
        return tuple(items)
