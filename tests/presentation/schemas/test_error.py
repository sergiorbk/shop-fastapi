from src.ecommerce.presentation.api.schemas import ErrorDetail, ErrorResponse


class TestErrorDetail:
    def test_error_detail(self):
        error = ErrorDetail(
            code=404,
            message="Not found",
            status="NOT_FOUND",
        )
        assert error.code == 404
        assert error.status == "NOT_FOUND"
        assert error.details is None

    def test_error_detail_with_details(self):
        error = ErrorDetail(
            code=422,
            message="Validation failed",
            status="INVALID_ARGUMENT",
            details=[{"field": "name", "reason": "required"}],
        )
        assert error.details is not None
        assert len(error.details) == 1


class TestErrorResponse:
    def test_error_response(self):
        response = ErrorResponse(
            error=ErrorDetail(
                code=500,
                message="Internal error",
                status="INTERNAL",
            )
        )
        assert response.error.code == 500
