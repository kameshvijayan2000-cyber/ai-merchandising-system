<<<<<<< HEAD
def calculate_piece_weight(
    garment_type,
    total_length,
    chest_or_thigh,
    sleeve_length,
    sleeve_width,
    gsm,
    extra_fabric
):

    if garment_type in ["T-Shirt Full Sleeve", "T-Shirt Half Sleeve"]:

        body_area = total_length * chest_or_thigh

        sleeve_area = 0
        if sleeve_length > 0 and sleeve_width > 0:
            sleeve_area = sleeve_length * sleeve_width

        total_area = (body_area + sleeve_area) * 2

        piece_weight = (total_area * gsm) / 10000 + extra_fabric

        return round(piece_weight, 3)

    elif garment_type == "Track Pant":

        total_area = total_length * chest_or_thigh * 4

        piece_weight = (total_area * gsm) / 10000 + extra_fabric

        return round(piece_weight, 3)

    return 0
=======
def calculate_piece_weight(
    garment_type,
    total_length,
    chest_or_thigh,
    sleeve_length,
    sleeve_width,
    gsm,
    extra_fabric
):

    if garment_type in ["T-Shirt Full Sleeve", "T-Shirt Half Sleeve"]:

        body_area = total_length * chest_or_thigh

        sleeve_area = 0
        if sleeve_length > 0 and sleeve_width > 0:
            sleeve_area = sleeve_length * sleeve_width

        total_area = (body_area + sleeve_area) * 2

        piece_weight = (total_area * gsm) / 10000 + extra_fabric

        return round(piece_weight, 3)

    elif garment_type == "Track Pant":

        total_area = total_length * chest_or_thigh * 4

        piece_weight = (total_area * gsm) / 10000 + extra_fabric

        return round(piece_weight, 3)

    return 0
>>>>>>> 542cdebd01ea9baf46f7d3618875dfb4a486bc55
