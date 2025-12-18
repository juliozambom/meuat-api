import math

def pagination(items, total_count, page, page_size):
    return {
        "metadata": {
            "page": page,
            "pageSize": page_size,
            "records": len(items),
            "totalPages": math.ceil(total_count / page_size),
            "totalRecords": total_count
        },
        "data": items
    }
