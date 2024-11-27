from scipy.signal import find_peaks

def detect_peaks_troughs(data, sensitivity = 5):
    """
    Detect peaks and troughs in stock data.
    :param data: List or Pandas Series of stock prices.
    :param sensitivity: Integer value controlling sensitivity (higher is less sensitive).
    :return: Indices of peaks and troughs.
    """
    try:
        # Peaks: Local maxima
        peaks, _ = find_peaks(data, height=sensitivity)

        # Troughs: Invert data to find local minima
        troughs, _ = find_peaks(-data, height=sensitivity)

        return peaks, troughs
    except Exception as e:
        raise RuntimeError(f"Error detecting peaks and troughs: {e}")
