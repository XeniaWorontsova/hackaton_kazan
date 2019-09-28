def list_to_dict(positions):
    result = {}
    for val in positions:
        result[val[0]] = val[1]
    return result