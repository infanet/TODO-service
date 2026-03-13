from fastapi import HTTPException, status

class AllError:
    def __init__(self, detail: str):
        self.detail = detail

    def not_found(self):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)

    def bad_request(self):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)