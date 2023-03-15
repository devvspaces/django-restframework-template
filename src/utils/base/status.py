"""
Descriptive HTTP status codes, for code api readability.
"""


class CustomStatusCode(object):
    @property
    def HTTP_200_OK(self) -> int:
        """Request is successful"""
        return 200

    @property
    def HTTP_201_CREATED(self) -> int:
        """Request is successful"""
        return 201

    @property
    def HTTP_400_BAD_REQUEST(self) -> int:
        """Error processing your request"""
        return 400

    @property
    def HTTP_401_FAILED_AUTHENTICATION(self) -> int:
        """Authentication credentials were not provided or not valid."""
        return 401

    @property
    def HTTP_403_FORBIDDEN(self) -> int:
        """You do not have permission to access this resource."""
        return 403

    @property
    def HTTP_404_NOT_FOUND(self) -> int:
        """Requested resource does not exist"""
        return 404

    # Custom error codes
    @property
    def HTTP_432_USER_NOT_FOUND(self) -> int:
        """User provided does not exist"""
        return 432

    @property
    def HTTP_433_INVALID_TOKEN(self) -> int:
        """Token passed is not valid"""
        return 433

    @property
    def HTTP_434_ALREADY_VERIFIED(self) -> int:
        """User has already been verified"""
        return 434

    @property
    def HTTP_435_INVALID_UIDB64(self) -> int:
        """uidb64 value passed is not valid"""
        return 435

    @property
    def HTTP_436_NO_ID(self) -> int:
        """ID value was not passed with the request"""
        return 436

    @property
    def HTTP_437_NO_EMAIL(self) -> int:
        """Email was not passed with the request"""
        return 437

    @property
    def HTTP_438_NOT_VERIFIED(self) -> int:
        """User email is not yet verified"""
        return 438

    @property
    def HTTP_439_ACCOUNT_DEACTIVATED(self) -> int:
        """Account has been deactivated"""
        return 439

    @property
    def HTTP_440_INVALID_SIGNATURE(self) -> int:
        """Invalid authorization code signature"""
        return 440

    @property
    def HTTP_441_NO_BUSINESS_ACCOUNT(self) -> int:
        """This user has no business account"""
        return 441

    @property
    def HTTP_442_BAD_PAYMENT_REQUEST(self) -> int:
        """Error creating payment charge"""
        return 442


StatCode = CustomStatusCode()
