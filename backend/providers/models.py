#
# class Wallet(BaseModel):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
#     name = models.CharField(max_length=255)
#     wallet_number = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
#     balance = models.DecimalField(
#         max_digits=32,
#         decimal_places=2,
#         validators=[MinValueValidator(0.0)],
#         default=Decimal("0.0"),
#     )
