def check_inventory(stock_levels, threshold):
    """
    Check inventory levels and generate reorder alerts if necessary.
    :param stock_levels: A dictionary containing the current stock levels of each item in the inventory.
    :param threshold: The threshold stock level at which a reorder alert should be generated.
    :return: A dictionary containing the items that need to be reordered along with their current stock levels.
    """
    items_to_reorder = {}
    for item, stock_level in stock_levels.items():
        if stock_level < threshold:
            items_to_reorder[item] = stock_level
    return items_to_reorder