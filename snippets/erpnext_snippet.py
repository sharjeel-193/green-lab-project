	
#accounts_controller.py ln 274, taken from ...
def init_internal_values(self):
    # init all the internal values as 0 on sa
    if self.docstatus.is_draft():
        # TODO: Add all such pending values here
        fields = ["billed_amt", "delivered_qty"]
        for item in self.get("items"):
            for field in fields:
                if hasattr(item, field):
                    item.set(field, 0)


def init_internal_values_unrolled(self):
    # init all the internal values as 0 on sa
    if self.docstatus.is_draft():
        # TODO: Add all such pending values here
        fields = ["billed_amt", "delivered_qty"]
        for item in self.get("items"):
            if hasattr(item, "billed_amt"):
                item.set("billed_amt", 0)
            if hasattr(item, "delivered_qty"):
                item.set("delivered_qty", 0)
