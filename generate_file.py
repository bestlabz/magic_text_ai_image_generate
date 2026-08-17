from magic_write import MagicWriteModel
import json

model = MagicWriteModel()
result = model.generate(
    "Sparkle",
    count=12,
    modern=True,
    output_type="fabric",
    generation_mode="modern_composition",
)
print(json.dumps(result, indent=2))
