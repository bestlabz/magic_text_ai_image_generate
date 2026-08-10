from magic_write import MagicWriteModel
import json

model = MagicWriteModel()
result = model.generate(
    "Sparkle",
    count=12,
    modern=True,
    output_type="fabric",
    generation_mode="ml",
    ml_model_path="magic_write_ml_model.pkl",
)

print(json.dumps(result, indent=2))
