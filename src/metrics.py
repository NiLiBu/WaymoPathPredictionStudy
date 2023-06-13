import math

# https://learnpainless.com/how-to-rotate-and-scale-a-vector-in-python/
def rotate_vector(vector, angle):
    x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
    y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
    return x, y


def calculateMissBoolean8s(xPredict, yPredict, vxStart, vyStart, xEnd, yEnd):
    """
    True if the target is not missed

    Args:
        xPredict (_type_): _description_
        yPredict (_type_): _description_
        vxStart (_type_): _description_
        vyStart (_type_): _description_
        xEnd (_type_): _description_
        yEnd (_type_): _description_

    Returns:
        _type_: _description_
    """
    initialSpeed = math.sqrt(vxStart*vxStart + vyStart * vyStart)
    
    speedAngle = math.atan2(vxStart,vyStart)/math.pi*180
    
    dx = xPredict - xEnd
    dy = yPredict - yEnd
    
    dLat, dLong = rotate_vector([dx, dy], speedAngle)
    
    AbsdLat = abs(dLat)
    AbsdLong = abs(dLong)
    
    # Metrics as defined in https://waymo.com/intl/en_us/open/challenges/2023/motion-prediction/
    # lateral 3m, longlitudinal 6m allowed
    if initialSpeed < 1.4:
        scale = 0.5
        if AbsdLat < scale * 3 and AbsdLong < scale * 6:
            return True
        else:
            return False
        
    elif initialSpeed < 11:
        alpha = (initialSpeed - 1.4)/(11 - 1.4)
        scale = 0.5 + 0.5 * alpha

        if AbsdLat < scale * 3 and AbsdLong < scale * 6:
            return True
        else:
            return False
    
    else:
        scale = 1
        if AbsdLat < scale * 3 and AbsdLong < scale * 6:
            return True
        else:
            return False
        
        
        
def calculateDisplacementError(xPredict, yPredict, vxStart, vyStart, xEnd, yEnd):
    """_summary_

    Args:
        xPredict (_type_): _description_
        yPredict (_type_): _description_
        vxStart (_type_): _description_
        vyStart (_type_): _description_
        xEnd (_type_): _description_
        yEnd (_type_): _description_

    Returns:
        _type_: _description_
    """
    speedAngle = math.atan2(vxStart,vyStart)/math.pi*180
    
    dx = xPredict - xEnd
    dy = yPredict - yEnd
    
    dLat, dLong = rotate_vector([dx, dy], speedAngle)
    return dLat, dLong