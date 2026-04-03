from math import ceil
def paginate(data:list, page:int, per_page:int) -> dict:
    total=len(data)
    total_pages = ceil (total/per_page) if total >0 else 1
    start = (page-1)*per_page
    end = start + per_page
    paginated = data[start:end]

    return{
        "total":        total,
        "total_pages":  total_pages,
        "current_page": page,
        "per_page":     per_page,
        "has_next":     page < total_pages,
        "has_prev":     page > 1,
        "data":         paginated
    }

def build_filter_query(
    course:  str  = None,
    grade:   str  = None,
    min_age: int  = None,
    max_age: int  = None,
    search:  str  = None) -> dict :
    query = {}

    # Filter by course (case insensitive)
    if course:
        query["course"] = {"$regex": course, "$options": "i"}

    # Filter by grade (case insensitive)
    if grade:
        query["grade"] = {"$regex": grade, "$options": "i"}

    # Filter by age range
    if min_age or max_age:
        query["age"] = {}
        if min_age:
            query["age"]["$gte"] = min_age
        if max_age:
            query["age"]["$lte"] = max_age

    # Search by name or email
    if search:
        query["$or"] = [
            {"name":  {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}}
        ]

    return query