from vehicle import euler


def test_euler():
    # when dv_dt is a positive number
    y_0 = 0
    dv_dt = 5
    h = 1
    assert euler(y_0, dv_dt, h) == (y_0 + dv_dt * h)

    # when dv_dt or h is zero
    assert euler(y_0, 0, h) == (y_0)
    assert euler(y_0, dv_dt, 0) == (y_0)
    assert euler(y_0, 0, 0) == (y_0)

    # when the previous y value is not zero
    y_0 = 5
    assert euler(y_0, dv_dt, h) == (y_0 + dv_dt * h)
