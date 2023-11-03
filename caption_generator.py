import pandas as pd
import sys
import random
from tqdm import tqdm
import os
import requests
sys.stdin.reconfigure(encoding='utf-8')
number_of_captions=10
e2b_mapping = {
    "5_o_Clock_Shadow": "হালকা_দাড়ি",
    "Arched_Eyebrows": "কুচকানো_ভ্রু",
    "Attractive": "আকর্ষণীয়",
    "Bags_Under_Eyes": "চোখের_নিচে_কালি",
    "Bald": "টাক",
    "Bangs": "কপালে_ছড়ানো_চুল",
    "Big_Lips": "বড়_ঠোঁট",
    "Big_Nose": "বড়_নাক",
    "Black_Hair": "কালো_চুল",
    "Blond_Hair": "সোনালী_চুল",
    "Blurry": "ঘোলা",
    "Brown_Hair": "বাদামী_চুল",
    "Bushy_Eyebrows": "ঘন_ভ্রু",
    "Chubby": "মোটা",
    "Double_Chin": "দ্বীত্ব_থুতনি",
    "Eyeglasses": "চশমা",
    "Goatee": "গোটি",
    "Gray_Hair": "ধূসর_চুল",
    "Heavy_Makeup": "ভারী_মেকাপ",
    "High_Cheekbones": "উঁচু_গালের_হাড়",
    "Male": "পুরুষ",
    "Mouth_Slightly_Open": "মুখ_কিছুটা_খোলা",
    "Mustache": "মোছ",
    "Narrow_Eyes": "সরু_চোখ",
    "No_Beard": "দাড়ি_নেই",
    "Oval_Face": "ডিম্বাকৃতির_চেহারা",
    "Pale_Skin": "ফ্যাকাশে",
    "Pointy_Nose": "চোখা_নাক",
    "Receding_Hairline": "সামনের_চুল_কম",
    "Rosy_Cheeks": "গোলাপী_গাল",
    "Sideburns": "জুলফি",
    "Smiling": "হাসি",
    "Straight_Hair": "সোজা_চুল",
    "Wavy_Hair": "ঢেউ_খেলানো_চুল",
    "Wearing_Earrings": "কানের_দুল_পরা",
    "Wearing_Hat": "টুপি_পরা",
    "Wearing_Lipstick": "লিপস্টিক_পরা",
    "Wearing_Necklace": "নেকলেস_পরা",
    "Wearing_Necktie": "টাই_পরা",
    "Young": "অল্পবয়স্ক"
}
ATTRIBUTES = {
    'IsAttributes': ['আকর্ষণীয়', 'টাক', 'ডিম্বাকৃতির চেহারা', 'অল্পবয়স্ক', 'হাসি','মোটা'],
    'HasAttributes': [
        'হালকা দাড়ি',
        'কুচকানো ভ্রু',
        'চোখের নিচে কালি',
        'কপালে ছড়ানো চুল',
        'বড় ঠোঁট',
        'বড় নাক',
        'কালো চুল',
        'সোনালী চুল',
        'ঘোলা',
        'বাদামী চুল',
        'ঘন ভ্রু',
        'দ্বীত্ব থুতনি',
        'চশমা',
        'গোটি',
        'ধূসর চুল',
        'উঁচু গালের হাড়',
        'মুখ কিছুটা খোলা',
        'মোছ',
        'সরু চোখ',
        'দাড়ি নেই',
        'ফ্যাকাশে',
        'চোখা নাক',
        'সামনের চুল কম',
        'গোলাপী গাল',
        'জুলফি',
        'সোজা চুল',
        'ঢেউ খেলানো চুল'
    ],
    'WearAttributes': [
        'কানের দুল পরা',
        'টুপি পরা',
        'লিপস্টিক পরা',
        'নেকলেস পরা',
        'টাই পরা',
        'ভারী মেকাপ'
    ],
    'Gender':[
         'পুরুষ'
    ]
}
def caption_template_1(gender,subjects,attributes,has_attr,is_attr,wear_attr,have):
 
    if "দাড়ি নেই" in has_attr:
        has_attr.remove("দাড়ি নেই")
    if "ঘোলা" in has_attr:
        has_attr.remove("ঘোলা")
        has_attr.append(random.choice(["চেহারা ঘোলা","মুখ ঘোলা"]))
    if "ফ্যাকাশে" in has_attr:
         has_attr.remove("ফ্যাকাশে")
         has_attr.append(random.choice(["চেহারা ফ্যাকাশে","মুখ ফ্যাকাশে"]))
    if "চশমা" in has_attr:
        has_attr.remove("চশমা")
        has_attr.append(random.choice(["চোখে চশমা","চোখে চশমা পরা"]))
    if "মোছ" in has_attr:
        has_attr.remove("মোছ")
        has_attr.append(random.choice(["মুখে মোছ"]))
    if "মুখ কিছুটা খোলা" in has_attr:
        has_attr.remove("মুখ কিছুটা খোলা")
        has_attr.append("কিছুটা খোলা মুখ")
    
    

    # abar edit korte hocche 
    if 'অল্পবয়স্ক' not in is_attr:
        if gender=="male":
            subjects[f'male_subjects_ro']=[
                "এই ব্যক্তির",
                "এই পুরুষের",
                "লোকটির",
                "এই ব্যাক্তিটির"
            ]
            subjects[f'male_subjects_ti']=[
                 "পুরুষটি",
                 "এই লোকটি"
            ]
        elif gender=="female":
         
            subjects[f'female_subjects_ro']=[
                "এই মহিলার",
                "মহিলাটির",
                "এই নারীর",
                "এই ব্যক্তির",
                "এই ব্যাক্তিটির"
            ]
            subjects[f'female_subjects_ti']=[
                 "মহিলাটি",
                 "এই ব্যাক্তিটি"
            ]
    elif "অল্পবয়স্ক" in is_attr:
        if gender=="male":
            subjects[f'male_subjects_ro']=['ছেলেটির','ছেলেটির','এই ব্যাক্তিটির','এই ব্যক্তির']
            subjects[f'male_subjects_ti']=['ছেলেটি','ছেলেটি','এই ব্যাক্তিটি']
        elif gender=="female":
            subjects[f'female_subjects_ro']=['মেয়েটির','মেয়েটির','এই ব্যাক্তিটির','এই ব্যক্তির']
            subjects[f'female_subjects_ti']=['মেয়েটি','মেয়েটি','এই ব্যাক্তিটি']
        
    # hair related attributes
    hair_props=[]
    hair_colors=[]
    hair_prop_names=[]
    for hair_prop in ["কালো চুল",'সোনালী চুল','ধূসর চুল','বাদামী চুল','সোজা চুল','ঢেউ খেলানো চুল']:
        if hair_prop in has_attr:
            if hair_prop=="সোজা চুল" or hair_prop=="ঢেউ খেলানো চুল":
                hair_props.append(" ".join(hair_prop.split(' ')[:-1]))
                hair_prop_names.append(hair_prop)
            else:
                hair_colors.append(" ".join(hair_prop.split(' ')[:-1]))
                hair_prop_names.append(hair_prop)
   
    if (len(hair_props)+len(hair_colors))>1:
        for hair_prop_name in hair_prop_names:
            has_attr.remove(hair_prop_name)
        
        random.shuffle(hair_props)
        random.shuffle(hair_colors)
        hair_prop_str="-".join(hair_colors)
        
        if len(hair_props)>0:
            hair_prop_str+=" ও "+"".join(hair_props)+" চুল"
        else:
            hair_prop_str+=" চুল"
        has_attr.append(hair_prop_str)
                 
     
    if len(has_attr)>1:
        random.shuffle(has_attr)
        last_attr=has_attr[-1]
        has_attr=", ".join(has_attr[:-1])
        has_attr+=" এবং "+last_attr
    elif len(has_attr)==1:
        has_attr=", ".join(has_attr)
    else:
        has_attr=None
    if has_attr is not None:
        part1=f"{random.choice(subjects[f'{gender}_subjects_ro'])} {has_attr} {random.choice(have)}।"
    else:
        part1=""
    part2=[]
    
    if 'টাক' in is_attr:
        part2.append(random.choice(["তার মাথায় টাক আছে।","তার টাক আছে।",
                                    f"{random.choice(subjects[f'{gender}_subjects_ro'])} টাক আছে।"]))
    if 'আকর্ষণীয়'  in is_attr:
        part2.append(random.choice(["সে দেখতে আকর্ষণীয়।","তাকে দেখতে আকর্ষণীয় মনে হচ্ছে।",
                                    f"{random.choice(subjects[f'{gender}_subjects_ti'])} আকর্ষণীয়।"]))
      
    if 'ডিম্বাকৃতির চেহারা'  in is_attr:
        part2.append(random.choice(["তার ডিম্বাকৃতির চেহারা দেখা যাচ্ছে।",
                                    "তার চেহারা ডিম্বাকৃতির।",
                                    "সে ডিম্বাকৃতির চেহারার অধিকারী।"]))
    if 'অল্পবয়স্ক' in is_attr:
        part2.append(random.choice(["সে অল্পবয়স্ক।",
                                    f"{random.choice(subjects[f'{gender}_subjects_ti'])} অল্পবয়স্ক।"]))
    if  'হাসি' in is_attr:
        part2.append(random.choice(["তার মুখে হাসি দেখা যাচ্ছে।",
                                    "তার চেহারায় হাসি দেখা যাচ্ছে।",
                                    f"এই ব্যাক্তিটির চেহারায় হাসি দেখা যাচ্ছে।"]))
    if 'মোটা' in is_attr:
        part2.append(random.choice([
             "তার চেহারা গোলগাল।",
             "সে দেখতে নাদুসনুদুস।",
        ]))
    random.shuffle(part2)
    if part2 is not None:
        part2=" ".join(part2)
    else:
        part2=""
    
    part3=[]
    if "কানের দুল পরা" in wear_attr:
            part3.append(random.choice([
                 "সে কানের দুল পরা।",
                 "সে কানের দুল পরে আছে।",
                 f"তাকে কানের দুল পরা {random.choice(['দেখা যাচ্ছে।','অবস্থায় দেখা যাচ্ছে।'])}",
                 f"{random.choice(subjects[f'{gender}_subjects_ti'])} কানের দুল পরা।"]))
    if "টুপি পরা" in wear_attr:
            part3.append(random.choice([
                 "সে টুপি পরা।",
                 f"তাকে {random.choice(['','মাথায়'])} টুপি পরা {random.choice(['দেখা যাচ্ছে।','অবস্থায় দেখা যাচ্ছে।'])}",
                 f"{random.choice(subjects[f'{gender}_subjects_ti'])} টুপি পরা।"]))
            
            
    if "লিপস্টিক পরা" in wear_attr:
            part3.append(random.choice([
                 f"তাকে {random.choice(['','ঠোঁটে'])} লিপস্টিক পরা অবস্থায় দেখা যাচ্ছে।",
                 f"তার ঠোঁটে লিপস্টিক পরা।",
                 f"{random.choice(subjects[f'{gender}_subjects_ti'])} {random.choice(['','ঠোঁটে'])} লিপস্টিক পরা।"]))
            
    if "নেকলেস পরা" in wear_attr:
            part3.append(random.choice([
                 f"তার {random.choice(['গলায়'])} নেকলেস পরা।",
                 f"তাকে {random.choice(['','গলায়'])} নেকলেস পরা {random.choice(['দেখা যাচ্ছে।','অবস্থায় দেখা যাচ্ছে।'])}",
                 f"{random.choice(subjects[f'{gender}_subjects_ti'])} {random.choice(['','গলায়'])} নেকলেস পরা।"]))
            
    if "টাই পরা" in wear_attr:
            part3.append(random.choice([
                 f"সে {random.choice(['','গলায়'])} টাই পরা।",
                 f"তাকে {random.choice(['','গলায়'])} টাই পরা {random.choice(['দেখা যাচ্ছে।','অবস্থায় দেখা যাচ্ছে।'])}",
                 f"{random.choice(subjects[f'{gender}_subjects_ti'])} {random.choice(['','গলায়'])} টাই পরা।"]))
            
    if "ভারী মেকাপ" in wear_attr:
            part3.append(random.choice([
                 f"তার {random.choice(['চেহারায়','মুখে'])} ভারী মেকাপ।",
                 f"তাকে ভারী মেকাপ পরা {random.choice(['দেখা যাচ্ছে।','অবস্থায় দেখা যাচ্ছে।'])}",
                 f"{random.choice(subjects[f'{gender}_subjects_ti'])} ভারী মেকাপ {random.choice(['পরা।','পরে আছে।'])}"
                 ]))
    random.shuffle(part3)
    if part3 is not None:
        part3=" ".join(part3)

    else:
        part3=""     
    if part1=="" and part2=="" and part3=="":
         if gender=="male":
              return f"একজন {random.choice(['লোক।','পুরুষ।','ছেলে।'])}"
         if gender=="female":
              return f"একজন {random.choice(['মহিলা।','নারী।','মেয়ে।'])}"
    final=random.choices([part1+' '+part2+' '+part3,
                          part1+' '+part3+' '+part2,
                          part2+' '+part3+' '+part1,
                          part3+' '+part2+' '+part1,
                          part2+' '+part1+' '+part3
                          ],weights=(50,50,3,3,2),k=1)[0]
    
    return final

def caption_generator(
      datas,
      col_to_attr_mappings,
      attr_to_col_mappings,
      col_names
            
):
    
   
    attributes=[col_to_attr_mappings[col_name] for i,col_name in enumerate(col_names) if datas[i]==1]
    #print(attributes)
    has_attr=[attribute for attribute in attributes if attribute in ATTRIBUTES['HasAttributes']]
    is_attr=[attribute for attribute in attributes if attribute in ATTRIBUTES['IsAttributes']]
    wear_attr=[attribute for attribute in attributes if attribute in ATTRIBUTES['WearAttributes']]

    male_subjects={
         "male_subjects_ro":[
            "এই ব্যক্তির",
            "এই পুরুষের",
            "লোকটির",
            "ছেলেটির",
            "এই ব্যাক্তিটির"# add non gender specific as last element
        ],
        "male_subjects_ti":[
              "পুরুষটি",
              "ছেলেটি",
        ],
         
    }
    female_subjects={
         "female_subjects_ro":[
            "এই মহিলার",
            "মহিলাটির",
            "মেয়েটির",
            "এই নারীর",
            "এই ব্যক্তির",
            "এই ব্যাক্তিটির" # try to keep the non gender specifics to the last position
        ],
        
        "female_subjects_ti":[
            "মহিলাটি",
            "মেয়েটি"
        ] 
    }
    have=[
         "রয়েছে",
         "আছে",
         "দেখা যাচ্ছে" 

    ]
    
    
    
    if "পুরুষ" in attributes:
        male_templates=[ caption_template_1("male",male_subjects,attributes,has_attr,is_attr,wear_attr,have)
                     for i in range(number_of_captions)
        ]
        #print(male_templates[0])
        return "\n".join(male_templates)
    else:
        female_templates=[
            caption_template_1("female",female_subjects,attributes,has_attr,is_attr,wear_attr,have)
            for i in range(number_of_captions)
        ]
        #print(female_templates[0])
        return "\n".join(female_templates)


if __name__=='__main__':
    files=os.listdir('.')
    attr_file_name="list_attr_celeba.csv"
    attr_file_url="ftp://example[.]com/list_attr_celeba.csv"
    if not attr_file_name in files:
        print("Downloading attribute file please wait....")
        response = requests.get(attr_file_url)
        if response.status_code == 200:
            with open(attr_file_name, "wb") as file:
                file.write(response.content)
            print(f"File '{attr_file_name}' has been downloaded and saved successfully.")
        else:
            print(f"Failed to download the file. HTTP Status Code: {response.status_code}")
            print(f"Please download this file from {attr_file_url}")
    
    #translating English attributes to Bengali
    attribute_datas=pd.read_csv(attr_file_name,delimiter=',')
    attribute_datas=attribute_datas.drop(columns=['image_id'])
    
    attribute_names=[e2b_mapping[attribute_name] for attribute_name in list(attribute_datas.columns)[0:]]
    #print(attribute_names)
    # Removing underscores from attributes and storing them in a new list
    cleaned_attributes = [attribute.replace("_", " ") for attribute in attribute_names]
    feature_names=cleaned_attributes
    #print(feature_names)
    mappings={}
    col_to_attr_mappings={k:v for k,v in zip(attribute_names,feature_names)}
    attr_to_col_mappings={v:k for k,v in zip(attribute_names,feature_names)}
    f = open("captions.txt", "w+",encoding='UTF-8')
    #print(attribute_datas)
    #print(len(attribute_datas.iloc[0,0:]))

    os.makedirs("captions",exist_ok=True)
    os.chdir('captions')
    
    print(f"Generating captions.....")
    for i in tqdm(range(0,len(attribute_datas))):
        face_info=attribute_datas.iloc[i,0:]

        #debug
        #face_info_json_english=face_info.copy()
        #face_info.index=feature_names
        #face_info_json_bangla=face_info
        
        face_info=list(face_info)
        #debug
        #print(face_info)
        caption_text=caption_generator(face_info,col_to_attr_mappings,attr_to_col_mappings,attribute_names)
        f_name=str(i+1).zfill(6)
        os.makedirs(f"{f_name}",exist_ok=True)
        os.chdir(f'{f_name}')
        f = open(f"{f_name}.txt", "w+",encoding='UTF-8')
        f.write(caption_text+"\n")
        f.close()
        
        #debug
        #face_info_json_bangla.to_csv(f'{i}_bangla.csv')
        #face_info_json_english.to_csv(f"{i}_english.csv")

        os.chdir('..')
    print("Done!")
