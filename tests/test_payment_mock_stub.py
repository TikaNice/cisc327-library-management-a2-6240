import pytest 
from unittest.mock import Mock
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway

#Define some common variables for fake return value
FAKE_book = {'book_id': 1, 'title': 'Test Book', 'available_copies': 1}
FAKE_patron_id = "123456"
FAKE_calculate_late_fee = {'fee_amount': 6.5, 'days_overdue': 10, 'status': 'Late fee calculated'}
FAKE_no_late_fee = {'fee_amount': 0.00, 'days_overdue': 0, 'status': 'No late fee'}


#Test pay_late_fees()
#Sucecess pay the late fees
def test_pay_late_fees_success(mocker):
    #Test successful payment of late fees.
    
    #Stub: fake late fee calculation
    mocker.patch("services.library_service.calculate_late_fee_for_book", 
        return_value=FAKE_calculate_late_fee
    )
    #Stub: fake book search
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value=FAKE_book
    )
    
    # Mock: fake payment gateway 
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123456_12345678", "Payment success")

    success, message, transaction = pay_late_fees(FAKE_patron_id, 1, mock_gateway)

    # Assert the result is as expected
    assert success is True
    assert transaction == "txn_123456_12345678"
    assert "Payment successful" in message
    
    # Verify process_payment function was called exactly once with expected parameters
    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(
        patron_id=FAKE_patron_id,
        amount=6.5,
        description="Late fees for 'Test Book'"
    )
    
#Test payment declined by gateway
def test_pay_late_fees_declied_by_gateway(mocker): 
    #Test payment declined by gateway
    
    #Stub: fake late fee calculation
    mocker.patch("services.library_service.calculate_late_fee_for_book", 
        return_value=FAKE_calculate_late_fee
    )
    #Stub: fake book search
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value=FAKE_book
    )
    
    # Mock: payment declined by gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, None, "Fail to make a payment")

    success, message, transaction = pay_late_fees(FAKE_patron_id, 1, mock_gateway)
    
    # Assert the result is as expected
    assert success is False
    assert transaction is None
    assert "Payment failed" in message
    
    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(
        patron_id=FAKE_patron_id,
        amount=6.5,
        description="Late fees for 'Test Book'"
    )

#Test invalid patron ID (verify mock NOT called)
def test_pay_late_fees_invalid_patron_id(mocker):
    """
    Invalid patron ID.
    Should fail before calling gateway (mock NOT called).
    """
    
    #Stub: fake late fee calculation
    # pay_late_fees() should detect invalid patron ID before call calculate_late_fee_for_book()
    mocker.patch("services.library_service.calculate_late_fee_for_book", 
        return_value=FAKE_calculate_late_fee
    )
    #Stub: fake book search
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value=FAKE_book
    )

    # Mock: fake payment gateway(sucess)
    # pay_late_fees() should detect invalid patron ID before call gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123456_12345678", "Payment success")

    # Assert the result is as expected
    success, message, txn = pay_late_fees("abc", 1, payment_gateway=mock_gateway)

    assert success is False
    assert txn is None
    assert "Invalid patron ID" in message
    #Shouldn't call gateway
    mock_gateway.process_payment.assert_not_called()

#Test zero late fees (verify mock NOT called)
def test_pay_late_fees_no_late_fee(mocker):
    """
    No late fee due.
    Should not call gateway (mock NOT called).
    """
    
    #Stub: no late fee
    mocker.patch("services.library_service.calculate_late_fee_for_book", 
        return_value=FAKE_no_late_fee
    )
    #Stub: fake book search
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value=FAKE_book
    )

    # Mock: fake payment gateway(sucess)
    # pay_late_fees() should detect no late fee and return fail before call gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123456_12345678", "Payment success")

    # Assert the result is as expected
    success, message, txn = pay_late_fees(FAKE_patron_id, 1, payment_gateway=mock_gateway)

    assert success is False
    assert txn is None
    assert "No late fees" in message
    #Shouldn't call gateway when no late fee
    mock_gateway.process_payment.assert_not_called()

#Test network error exception handling
def test_pay_late_fees_network_error(mocker):
    """
    Network error.
    Should catch network error and return fail without calling gateway.
    """
    
    #Stub: fake late fee calculation
    mocker.patch("services.library_service.calculate_late_fee_for_book", 
        return_value=FAKE_calculate_late_fee
    )
    #Stub: fake book search
    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value=FAKE_book
    )

    # Mock: fake payment gateway(fail)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network unreachable")

    # Assert the result is as expected
    success, message, txn = pay_late_fees(FAKE_patron_id, 1, payment_gateway=mock_gateway)

    assert success is False
    assert txn is None
    assert "Payment processing error" in message
    
    mock_gateway.process_payment.assert_called_once()


#Test refund_late_fee_payment()
#Test successful refund
def test_refund_late_fee_success(mocker):
    #Test successful refund
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund successful")
    
    #Use 12345678 as the time of payment
    #Use 123456 as patron_id
    success, message = refund_late_fee_payment("txn_123456_12345678", 5.00, payment_gateway=mock_gateway)

    # Assert the result is as expected
    assert success is True
    assert "Refund successful" in message
    
    mock_gateway.refund_payment.assert_called_once()
    mock_gateway.refund_payment.assert_called_with(
        "txn_123456_12345678", 
        5.00
    )

def test_refund_invalid_transaction_id_rejected(mocker):
    #Invalid transaction IDs are rejected and gateway not called.
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund successful")
    
    #The transaction ID is invalid(not start with tvn)
    success, message = refund_late_fee_payment("invaild", 5.0, payment_gateway=mock_gateway)
    
    assert success is False
    assert "Invalid transaction ID" in message
    #The gateway should not be called.
    mock_gateway.refund_payment.assert_not_called()
    
#Test invalid negative refund amount
def test_refund_invalid_negative_amounts_rejected(mocker):
    """Negative amounts should be rejected without calling gateway."""
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_123456_12345678", -4, payment_gateway=mock_gateway)
    
    assert success is False
    assert "Refund amount must be greater than 0" in message
    #Should return fail without calling gateway
    mock_gateway.refund_payment.assert_not_called()

#Test invalid 0 refund amount
def test_refund_invalid_0_amounts_rejected(mocker):
    """0 amounts should be rejected without calling gateway."""
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_123456_12345678", 0, payment_gateway=mock_gateway)
    
    assert success is False
    assert "Refund amount must be greater than 0" in message
    #Should return fail without calling gateway
    mock_gateway.refund_payment.assert_not_called()

#Test invalid more than 15$ refund amount
def test_refund_invalid_more_than_15_amounts_rejected(mocker):
    """More than 15$ amounts should be rejected without calling gateway."""
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_123456_12345678", 20, payment_gateway=mock_gateway)
    
    assert success is False
    assert "Refund amount exceeds maximum late fee" in message
    #Should return fail without calling gateway
    mock_gateway.refund_payment.assert_not_called()
