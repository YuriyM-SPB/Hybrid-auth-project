# Fuse context risk and keystroke risk into one combined risk

def fuse_risks(context_risk, keystroke_risk, w_context=0.5, w_keystroke=0.5):
    combined = (w_context * context_risk) + (w_keystroke * keystroke_risk)
    return combined