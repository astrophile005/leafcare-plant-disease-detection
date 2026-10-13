"""
knowledge.py - plain-language information about each condition the model can detect.

The model's class names look like "Tomato___Late_blight". get_info() splits those into
a crop and a condition and attaches the notes below. The notes are general guidance only.
"""
import re


def _key(text: str) -> str:
    """Normalise a name so 'Common_rust_' and 'Common rust' match the same entry."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _entry(name, kind, symptoms, actions):
    return {"name": name, "type": kind, "symptoms": symptoms, "actions": actions}


INFO = {
    _key("Apple_scab"): _entry(
        "Apple scab", "Fungal",
        "Olive-green to brown velvety spots on leaves, and rough, scabby patches on fruit.",
        [
            "Rake up and destroy fallen leaves in autumn, since the fungus overwinters there.",
            "Prune to open the canopy so leaves dry quickly.",
            "Choose scab-resistant varieties when planting.",
            "If needed, use a fungicide at the timing recommended by your local agriculture office.",
        ],
    ),
    _key("Black_rot"): _entry(
        "Black rot", "Fungal",
        "Brown to black spots on leaves, often with darker borders. Fruit can shrivel into hard black 'mummies'.",
        [
            "Remove and destroy infected leaves, mummified fruit and dead wood.",
            "Improve air flow by pruning, and avoid wetting the leaves when watering.",
            "Protective fungicide sprays at the right growth stage can help; follow the label and local advice.",
        ],
    ),
    _key("Cedar_apple_rust"): _entry(
        "Cedar apple rust", "Fungal",
        "Bright yellow-orange spots on the upper leaf surface, sometimes with small tube-like growths underneath.",
        [
            "The fungus needs both apple and juniper/cedar trees, so remove nearby junipers if practical.",
            "Plant rust-resistant apple varieties.",
            "Fungicide in spring, when leaves open, can protect new growth; check local guidance.",
        ],
    ),
    _key("Powdery_mildew"): _entry(
        "Powdery mildew", "Fungal",
        "A white or grey powdery coating on leaves and young shoots; leaves may curl or become distorted.",
        [
            "Prune for good air circulation and avoid crowding plants.",
            "Remove badly affected leaves and shoots.",
            "Sulfur or other fungicides labelled for your crop can help; follow the label.",
        ],
    ),
    _key("Cercospora_leaf_spot Gray_leaf_spot"): _entry(
        "Cercospora / Gray leaf spot", "Fungal",
        "Narrow, rectangular grey to tan spots running between the leaf veins.",
        [
            "Rotate crops and manage crop residue, since the fungus survives in old corn debris.",
            "Plant hybrids with resistance to gray leaf spot.",
            "Fungicide may be worthwhile in severe, humid seasons; ask your local extension service.",
        ],
    ),
    _key("Common_rust_"): _entry(
        "Common rust", "Fungal",
        "Small, powdery reddish-brown pustules scattered on both sides of the leaf.",
        [
            "Plant resistant hybrids where rust is common.",
            "Scout early; mild infections often do little damage.",
            "Fungicide is only worth considering when infection starts early and is heavy.",
        ],
    ),
    _key("Northern_Leaf_Blight"): _entry(
        "Northern leaf blight", "Fungal",
        "Long, cigar-shaped grey-green to tan lesions on the leaves.",
        [
            "Use resistant hybrids and rotate crops.",
            "Bury or manage residue after harvest.",
            "Fungicide can help in serious outbreaks; follow local recommendations.",
        ],
    ),
    _key("Esca_(Black_Measles)"): _entry(
        "Esca (Black measles)", "Fungal (disease complex)",
        "Yellow or brown 'tiger-stripe' patterns on leaves, and dark spots on berries.",
        [
            "There is no cure, so protect vines by pruning in dry weather and sealing large pruning wounds.",
            "Remove and destroy badly affected vines or arms.",
            "Reduce vine stress with good watering and nutrition.",
        ],
    ),
    _key("Leaf_blight_(Isariopsis_Leaf_Spot)"): _entry(
        "Leaf blight (Isariopsis leaf spot)", "Fungal",
        "Dark brown to black angular spots on leaves that can lead to early leaf drop.",
        [
            "Clear fallen leaves and trim the canopy so it dries quickly.",
            "Avoid overhead watering.",
            "Use fungicide if the disease keeps returning; follow local advice.",
        ],
    ),
    _key("Haunglongbing_(Citrus_greening)"): _entry(
        "Citrus greening (Huanglongbing)", "Bacterial, spread by insects",
        "Blotchy yellow mottling of leaves, small lopsided fruit that stays green and tastes bitter.",
        [
            "There is no cure. Infected trees are usually removed to protect others.",
            "Control the Asian citrus psyllid insect that spreads the disease.",
            "Report suspected cases to your local agriculture authority and use disease-free nursery plants.",
        ],
    ),
    _key("Bacterial_spot"): _entry(
        "Bacterial spot", "Bacterial",
        "Small, dark, water-soaked spots on leaves (sometimes with a yellow halo). Spots can fall out, leaving holes.",
        [
            "Start with disease-free seed or plants.",
            "Avoid overhead watering and don't work among wet plants.",
            "Copper-based sprays may slow spread; follow the label.",
            "Rotate crops and remove infected plant debris.",
        ],
    ),
    _key("Early_blight"): _entry(
        "Early blight", "Fungal",
        "Brown spots with concentric rings (like a target), usually starting on older, lower leaves.",
        [
            "Remove infected lower leaves and clear plant debris at season's end.",
            "Mulch to stop soil splashing onto leaves, and water at the base.",
            "Rotate crops and give plants enough space.",
            "Fungicide may be needed in humid weather; follow local advice.",
        ],
    ),
    _key("Late_blight"): _entry(
        "Late blight", "Oomycete (water mold)",
        "Dark, water-soaked blotches that spread quickly; white fuzzy growth may appear underneath in humid weather.",
        [
            "Act quickly: this disease can destroy a crop within days.",
            "Remove and destroy infected plants. Don't compost them.",
            "Keep foliage dry and avoid overhead watering.",
            "Protective fungicides can help; ask your local extension service for the right product and timing.",
        ],
    ),
    _key("Leaf_scorch"): _entry(
        "Leaf scorch", "Fungal",
        "Many small purple spots that merge, with leaf edges turning brown as if scorched.",
        [
            "Remove old infected leaves after harvest.",
            "Space plants for air flow and avoid overhead watering.",
            "Plant resistant varieties and use clean planting stock.",
        ],
    ),
    _key("Leaf_Mold"): _entry(
        "Leaf mold", "Fungal",
        "Pale yellow patches on the upper leaf surface, with olive-brown velvety mold underneath.",
        [
            "Improve ventilation and reduce humidity, especially in greenhouses.",
            "Water at the base and avoid wetting leaves.",
            "Use resistant varieties and remove affected leaves.",
        ],
    ),
    _key("Septoria_leaf_spot"): _entry(
        "Septoria leaf spot", "Fungal",
        "Many small round spots with grey centres and dark edges, often with tiny black dots inside.",
        [
            "Remove infected lower leaves and clear debris.",
            "Mulch and water at the base to limit splash.",
            "Rotate crops; fungicide can help in wet seasons.",
        ],
    ),
    _key("Spider_mites Two-spotted_spider_mite"): _entry(
        "Spider mites (two-spotted)", "Pest (not a disease)",
        "Tiny pale speckles on leaves, bronzing, and fine webbing, especially in hot, dry conditions.",
        [
            "Rinse leaves with a strong water spray, including the undersides.",
            "Insecticidal soap or a miticide labelled for your crop can help; follow the label.",
            "Keep plants well watered and avoid dusty conditions; protect natural predators.",
        ],
    ),
    _key("Target_Spot"): _entry(
        "Target spot", "Fungal",
        "Brown spots with rings like a target on leaves, which may also appear on stems and fruit.",
        [
            "Prune for air flow and remove infected leaves.",
            "Avoid overhead watering and rotate crops.",
            "Fungicide may be needed in humid weather; follow local advice.",
        ],
    ),
    _key("Tomato_mosaic_virus"): _entry(
        "Tomato mosaic virus", "Viral",
        "Mottled light and dark green patches on leaves, sometimes with curled, narrow or distorted growth.",
        [
            "There is no cure, so remove and destroy infected plants.",
            "Wash hands and disinfect tools, especially after handling tobacco products.",
            "Choose resistant varieties and clean seed.",
        ],
    ),
    _key("Tomato_Yellow_Leaf_Curl_Virus"): _entry(
        "Tomato yellow leaf curl virus", "Viral, spread by whiteflies",
        "Leaves curl upward and turn yellow, and plants are stunted with few fruit.",
        [
            "There is no cure, so remove infected plants.",
            "Control whiteflies with insect-proof netting, reflective mulch or approved insecticides.",
            "Plant resistant varieties.",
        ],
    ),
}

HEALTHY = _entry(
    "Healthy", "-",
    "No visible signs of disease were detected on this leaf.",
    [
        "Keep checking your plants regularly, since early detection makes treatment easier.",
        "Water at the base of the plant and avoid wetting the leaves late in the day.",
        "Give plants enough space for air to move, and remove fallen debris.",
    ],
)


def _pretty_crop(raw: str) -> str:
    return raw.replace(",_", ", ").replace("_(", " (").replace("_", " ")


def get_info(class_name: str) -> dict:
    """Turn a class name like 'Tomato___Late_blight' into display-ready info."""
    crop_raw, _, disease_raw = class_name.partition("___")
    crop = _pretty_crop(crop_raw)

    if _key(disease_raw) == "healthy":
        return {"crop": crop, "condition": "Healthy", "healthy": True, "details": HEALTHY}

    details = INFO.get(_key(disease_raw))
    condition = details["name"] if details else disease_raw.replace("_", " ").strip()
    return {"crop": crop, "condition": condition, "healthy": False, "details": details}