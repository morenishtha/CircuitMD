
import gradio as gr

RESPONSES = {
    "power_supply_low": "Your LDO voltage regulator is in dropout mode. Check: 1) Input voltage (need >5.5V), 2) Load current (exceeds max?), 3) Bypass capacitor (low ESR?). Solutions: Use buck converter, increase input voltage to 9V+, or add larger output capacitor. Safety: Ensure proper heatsinking!",
    
    "power_supply_hot": "Regulator dissipating too much power. Likely cause: 1) Load current too high for linear reg, 2) Input voltage too high, 3) Poor thermal path. Fixes: Reduce input voltage, switch to buck converter, add heatsink with thermal compound, or reduce load current. Linear regs with high power = always hot. Use buck converters!",
    
    "signal_integrity": "Signal integrity issues from: 1) Poor trace routing (too long), 2) Insufficient decoupling caps, 3) Ground plane disconnects, 4) Slow rise/fall times. Diagnose: Use oscilloscope for ringing/overshoot. Solutions: Keep traces short, add 100nF caps near ICs, maintain continuous ground plane, match impedance for high-speed signals.",
    
    "led_flicker": "LED flicker from: 1) Unstable power supply (voltage sag), 2) Low PWM frequency (<100Hz visible), 3) Poor current limiting. Check: Is power sagging? Add larger cap. Is it PWM? Increase frequency >500Hz. Current limiting? Use resistors or current sources. With linear reg + high current LEDs → switch to buck converter.",
    
    "component_hot": "Component overheating: 1) Check max ratings (voltage, current, power), 2) Verify thermal pathway (heatsink?), 3) Check for shorts nearby. Solutions: Reduce current/voltage, add heatsink with thermal compound, increase airflow, switch to higher-rated component. PCB layout matters—surround component with copper pour to ground!",
    
    "default": "CircuitMD here! I can help troubleshoot circuits. Tell me: 1) Circuit type (power supply, signal, RF), 2) What's failing (voltage wrong, hot, signal issues), 3) Any measurements. I can help with voltage regulation, signal integrity, overheating, PCB layout, thermal management. What's happening with your circuit?"
}

def get_diagnosis(symptom, circuit_type):
    """Match symptoms to hardcoded responses"""
    symptom_lower = symptom.lower()
    
    if circuit_type == "Power Supply" or "power" in symptom_lower:
        if any(word in symptom_lower for word in ["3v", "low", "drop", "less than", "only"]):
            return RESPONSES["power_supply_low"]
        elif any(word in symptom_lower for word in ["hot", "heat", "warm"]):
            return RESPONSES["power_supply_hot"]
    
    if circuit_type == "Signal" or "signal" in symptom_lower:
        if any(word in symptom_lower for word in ["ring", "noise", "integrity"]):
            return RESPONSES["signal_integrity"]
    
    if any(word in symptom_lower for word in ["led", "flicker", "blink"]):
        return RESPONSES["led_flicker"]
    
    if any(word in symptom_lower for word in ["hot", "heat", "temperature"]):
        return RESPONSES["component_hot"]
    
    return RESPONSES["default"]

# Create Gradio interface
with gr.Blocks(title="CircuitMD") as demo:
    gr.Markdown("# 🔧 CircuitMD - Expert Circuit Troubleshooting")
    gr.Markdown("Describe your circuit problem and get instant expert diagnosis!")
    
    with gr.Row():
        circuit_type = gr.Dropdown(
            choices=["Power Supply", "Signal", "RF", "General"],
            value="Power Supply",
            label="Circuit Type"
        )
    
    symptom = gr.Textbox(
        label="Describe your circuit problem",
        placeholder="E.g., My 5V power supply is only outputting 3V...",
        lines=3
    )
    
    submit_btn = gr.Button("Get Diagnosis", variant="primary")
    
    diagnosis = gr.Textbox(
        label="CircuitMD Diagnosis",
        interactive=False,
        lines=6
    )
    
    submit_btn.click(
        fn=get_diagnosis,
        inputs=[symptom, circuit_type],
        outputs=diagnosis
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)