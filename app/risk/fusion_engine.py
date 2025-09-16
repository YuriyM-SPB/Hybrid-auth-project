# Fuse context risk and keystroke risk into one combined risk

def fuse_risks(context_risk, keystroke_risk, context_threshold=0.8, keystroke_threshold=0.8):
    combined = max(context_risk, keystroke_risk)
    needs_stepup = (context_risk >= context_threshold) or (keystroke_risk >= keystroke_threshold)
    return combined, needs_stepup