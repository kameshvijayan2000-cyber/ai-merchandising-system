import pandas as pd
print("NEW FABRIC PROGRAM LOADED")
def calculate_fabric_program(
    total_qty,
    color_ratios,
    body_weight,
    rib_weight,
    sj_weight,
    extra_percent,
    body_loss,
    rib_loss,
    sj_loss
):
    results = []

    # Total ratio units
    total_ratio_units = 0
    for color in color_ratios:
        total_ratio_units += sum(color_ratios[color].values())

    base_value = total_qty / total_ratio_units

    for color, sizes in color_ratios.items():

        color_summary = {
            "Color": color,
            "Body Total (Kg)": 0,
            "Rib Total (Kg)": 0,
            "SJ Total (Kg)": 0
        }

        for size, ratio in sizes.items():

            order_qty = ratio * base_value

            # 7% Extra
            adjusted_qty = order_qty * (1 + extra_percent / 100)

            # BODY
            body_final = 0
            if body_weight > 0:
                body_fabric = adjusted_qty * body_weight
                body_final = body_fabric * (1 + body_loss / 100)
                color_summary["Body Total (Kg)"] += body_final

            # RIB
            rib_final = 0
            if rib_weight > 0:
                rib_fabric = adjusted_qty * rib_weight
                rib_final = rib_fabric * (1 + rib_loss / 100)
                color_summary["Rib Total (Kg)"] += rib_final

            # SJ
            sj_final = 0
            if sj_weight > 0:
                sj_fabric = adjusted_qty * sj_weight
                sj_final = sj_fabric * (1 + sj_loss / 100)
                color_summary["SJ Total (Kg)"] += sj_final

        # Round totals
        color_summary["Body Total (Kg)"] = round(color_summary["Body Total (Kg)"], 2)
        color_summary["Rib Total (Kg)"] = round(color_summary["Rib Total (Kg)"], 2)
        color_summary["SJ Total (Kg)"] = round(color_summary["SJ Total (Kg)"], 2)

        results.append(color_summary)

    df = pd.DataFrame(results)
    return df
