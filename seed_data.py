import json
from models import get_db

def seed_all():
    conn = get_db()
    cursor = conn.cursor()

    # Check if already seeded
    count = cursor.execute('SELECT COUNT(*) FROM vocabulary').fetchone()[0]
    if count > 0:
        conn.close()
        return

    # ═══════════════════════════════════════════
    # VOCABULARY - Wide variety per level
    # ═══════════════════════════════════════════

    vocabulary_data = [
        # ── A1 - Beginner ──
        # Daily Life
        ("hello", "A greeting used when meeting someone", "merhaba", "Hello! How are you today?", "Merhaba! Bugün nasılsın?", "A1", "Greetings", "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=300"),
        ("goodbye", "A word used when leaving someone", "hoşça kal", "Goodbye! See you tomorrow.", "Hoşça kal! Yarın görüşürüz.", "A1", "Greetings", None),
        ("please", "A polite word used when asking for something", "lütfen", "Can I have some water, please?", "Biraz su alabilir miyim, lütfen?", "A1", "Greetings", None),
        ("thank you", "An expression of gratitude", "teşekkür ederim", "Thank you for helping me.", "Bana yardım ettiğin için teşekkür ederim.", "A1", "Greetings", None),
        ("sorry", "An expression of apology", "özür dilerim", "I'm sorry for being late.", "Geç kaldığım için özür dilerim.", "A1", "Greetings", None),
        ("yes", "An affirmative response", "evet", "Yes, I would like some tea.", "Evet, biraz çay istiyorum.", "A1", "Greetings", None),
        ("no", "A negative response", "hayır", "No, I don't want any coffee.", "Hayır, kahve istemiyorum.", "A1", "Greetings", None),

        # Family
        ("mother", "A female parent", "anne", "My mother cooks delicious food.", "Annem lezzetli yemekler pişirir.", "A1", "Family", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300"),
        ("father", "A male parent", "baba", "My father works in an office.", "Babam bir ofiste çalışıyor.", "A1", "Family", None),
        ("brother", "A male sibling", "erkek kardeş", "I have one brother and one sister.", "Bir erkek kardeşim ve bir kız kardeşim var.", "A1", "Family", None),
        ("sister", "A female sibling", "kız kardeş", "My sister is older than me.", "Kız kardeşim benden büyük.", "A1", "Family", None),
        ("family", "A group of related people", "aile", "I love spending time with my family.", "Ailemle vakit geçirmeyi seviyorum.", "A1", "Family", "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=300"),
        ("friend", "A person you like and trust", "arkadaş", "She is my best friend.", "O benim en iyi arkadaşım.", "A1", "Family", None),
        ("baby", "A very young child", "bebek", "The baby is sleeping now.", "Bebek şimdi uyuyor.", "A1", "Family", None),

        # Food
        ("water", "A clear liquid for drinking", "su", "Can I have a glass of water?", "Bir bardak su alabilir miyim?", "A1", "Food", "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300"),
        ("bread", "A food made from flour", "ekmek", "I eat bread for breakfast.", "Kahvaltıda ekmek yerim.", "A1", "Food", "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"),
        ("apple", "A round red or green fruit", "elma", "I eat an apple every day.", "Her gün bir elma yerim.", "A1", "Food", "https://images.unsplash.com/photo-1568702846914-96b305d2uj38?w=300"),
        ("milk", "A white liquid from cows", "süt", "Children should drink milk.", "Çocuklar süt içmelidir.", "A1", "Food", None),
        ("rice", "Small white grains used as food", "pirinç", "We eat rice with vegetables.", "Sebzelerle birlikte pirinç yeriz.", "A1", "Food", None),
        ("egg", "An oval object laid by a bird", "yumurta", "I had two eggs for breakfast.", "Kahvaltıda iki yumurta yedim.", "A1", "Food", None),
        ("chicken", "A bird kept for meat and eggs", "tavuk", "We are having chicken for dinner.", "Akşam yemeğinde tavuk yiyeceğiz.", "A1", "Food", None),
        ("coffee", "A hot brown drink", "kahve", "I drink coffee every morning.", "Her sabah kahve içerim.", "A1", "Food", None),
        ("tea", "A hot drink made from leaves", "çay", "Would you like some tea?", "Biraz çay ister misiniz?", "A1", "Food", None),
        ("sugar", "A sweet white substance", "şeker", "Do you take sugar in your tea?", "Çayına şeker alır mısın?", "A1", "Food", None),

        # Numbers & Time
        ("today", "This current day", "bugün", "Today is a beautiful day.", "Bugün güzel bir gün.", "A1", "Time", None),
        ("tomorrow", "The day after today", "yarın", "I will visit you tomorrow.", "Yarın seni ziyaret edeceğim.", "A1", "Time", None),
        ("yesterday", "The day before today", "dün", "I went to school yesterday.", "Dün okula gittim.", "A1", "Time", None),
        ("morning", "The early part of the day", "sabah", "Good morning! Did you sleep well?", "Günaydın! İyi uyudun mu?", "A1", "Time", None),
        ("night", "The dark part of the day", "gece", "Good night! Sleep well.", "İyi geceler! İyi uykular.", "A1", "Time", None),
        ("week", "A period of seven days", "hafta", "I have exams next week.", "Gelecek hafta sınavlarım var.", "A1", "Time", None),

        # Places
        ("school", "A place where children learn", "okul", "I go to school every day.", "Her gün okula giderim.", "A1", "Places", "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=300"),
        ("house", "A building where people live", "ev", "Our house has three bedrooms.", "Evimizin üç yatak odası var.", "A1", "Places", "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=300"),
        ("hospital", "A place where sick people go", "hastane", "The hospital is near my house.", "Hastane evimin yakınında.", "A1", "Places", None),
        ("park", "An area of land for recreation", "park", "Children play in the park.", "Çocuklar parkta oynuyor.", "A1", "Places", None),
        ("shop", "A place where things are sold", "dükkan", "I bought this from a shop.", "Bunu bir dükkandan aldım.", "A1", "Places", None),
        ("restaurant", "A place where you can buy meals", "restoran", "Let's eat at a restaurant.", "Bir restoranda yemek yiyelim.", "A1", "Places", None),

        # Body & Clothes
        ("head", "The top part of your body", "baş/kafa", "I have a hat on my head.", "Başımda bir şapka var.", "A1", "Body", None),
        ("hand", "The part at the end of your arm", "el", "Please wash your hands.", "Lütfen ellerinizi yıkayın.", "A1", "Body", None),
        ("eye", "The organ used for seeing", "göz", "She has blue eyes.", "Mavi gözleri var.", "A1", "Body", None),
        ("shirt", "Clothing for the upper body", "gömlek", "He is wearing a blue shirt.", "Mavi bir gömlek giyiyor.", "A1", "Clothes", None),
        ("shoes", "Covering for the feet", "ayakkabı", "These shoes are very comfortable.", "Bu ayakkabılar çok rahat.", "A1", "Clothes", None),

        # ── A2 - Elementary ──
        # Travel
        ("airport", "A place where planes take off and land", "havalimanı", "We arrived at the airport early.", "Havalimanına erken vardık.", "A2", "Travel", "https://images.unsplash.com/photo-1436491865332-7a61a109db05?w=300"),
        ("ticket", "A paper that allows you to travel", "bilet", "I bought a train ticket online.", "İnternetten tren bileti aldım.", "A2", "Travel", None),
        ("passport", "An official document for international travel", "pasaport", "Don't forget your passport!", "Pasaportunu unutma!", "A2", "Travel", None),
        ("luggage", "Bags and suitcases for traveling", "bavul/bagaj", "My luggage is very heavy.", "Bavulum çok ağır.", "A2", "Travel", None),
        ("vacation", "A period of rest from work", "tatil", "We went on vacation to Spain.", "İspanya'ya tatile gittik.", "A2", "Travel", None),
        ("journey", "Traveling from one place to another", "yolculuk", "The journey took about three hours.", "Yolculuk yaklaşık üç saat sürdü.", "A2", "Travel", None),
        ("map", "A drawing showing an area", "harita", "I used a map to find the hotel.", "Oteli bulmak için harita kullandım.", "A2", "Travel", None),
        ("hotel", "A building where travelers stay", "otel", "We booked a room at the hotel.", "Otelde bir oda rezerve ettik.", "A2", "Travel", None),

        # Work & Education
        ("office", "A room where people work", "ofis", "She works in a big office.", "Büyük bir ofiste çalışıyor.", "A2", "Work", None),
        ("meeting", "A gathering of people to discuss something", "toplantı", "We have a meeting at 2 PM.", "Saat 2'de toplantımız var.", "A2", "Work", None),
        ("salary", "Money paid for work", "maaş", "She earns a good salary.", "İyi bir maaş kazanıyor.", "A2", "Work", None),
        ("manager", "A person who controls a team", "müdür/yönetici", "The manager approved my request.", "Müdür talebimi onayladı.", "A2", "Work", None),
        ("university", "A place of higher education", "üniversite", "I want to study at university.", "Üniversitede okumak istiyorum.", "A2", "Education", "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=300"),
        ("exam", "A formal test of knowledge", "sınav", "I have a math exam tomorrow.", "Yarın matematik sınavım var.", "A2", "Education", None),
        ("homework", "School work done at home", "ödev", "Did you finish your homework?", "Ödevini bitirdin mi?", "A2", "Education", None),
        ("subject", "An area of study", "ders/konu", "My favorite subject is science.", "En sevdiğim ders fen bilimleri.", "A2", "Education", None),
        ("library", "A place with many books", "kütüphane", "I study at the library.", "Kütüphanede ders çalışırım.", "A2", "Education", "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=300"),
        ("degree", "A qualification from university", "diploma/derece", "She has a degree in engineering.", "Mühendislik diploması var.", "A2", "Education", None),

        # Health
        ("medicine", "A substance used to treat illness", "ilaç", "Take this medicine after meals.", "Bu ilacı yemeklerden sonra al.", "A2", "Health", None),
        ("headache", "A pain in the head", "baş ağrısı", "I have a terrible headache.", "Korkunç bir baş ağrım var.", "A2", "Health", None),
        ("exercise", "Physical activity for fitness", "egzersiz", "Exercise is good for your health.", "Egzersiz sağlığınız için iyidir.", "A2", "Health", None),
        ("healthy", "In good physical condition", "sağlıklı", "Eating vegetables keeps you healthy.", "Sebze yemek sizi sağlıklı tutar.", "A2", "Health", None),
        ("tired", "Needing rest or sleep", "yorgun", "I am very tired after work.", "İşten sonra çok yorgunum.", "A2", "Health", None),
        ("fever", "A high body temperature", "ateş", "He stayed home because of a fever.", "Ateşi olduğu için evde kaldı.", "A2", "Health", None),

        # Weather & Nature
        ("weather", "The state of the atmosphere", "hava durumu", "The weather is nice today.", "Bugün hava güzel.", "A2", "Weather", None),
        ("rain", "Water falling from clouds", "yağmur", "It started to rain heavily.", "Şiddetli yağmur yağmaya başladı.", "A2", "Weather", "https://images.unsplash.com/photo-1515694346937-94d85e39d29?w=300"),
        ("sunny", "Bright with sunlight", "güneşli", "It's a beautiful sunny day.", "Güzel güneşli bir gün.", "A2", "Weather", None),
        ("cloud", "A white or grey mass in the sky", "bulut", "There are dark clouds in the sky.", "Gökyüzünde kara bulutlar var.", "A2", "Weather", None),
        ("snow", "Frozen water that falls from clouds", "kar", "The children love playing in the snow.", "Çocuklar karda oynamayı seviyor.", "A2", "Weather", None),
        ("wind", "Moving air", "rüzgar", "The wind is very strong today.", "Bugün rüzgar çok güçlü.", "A2", "Weather", None),
        ("mountain", "A very high hill", "dağ", "We climbed the mountain last summer.", "Geçen yaz dağa tırmandık.", "A2", "Nature", None),
        ("river", "A large flow of water", "nehir", "We swam in the river.", "Nehirde yüzdük.", "A2", "Nature", None),
        ("forest", "A large area covered with trees", "orman", "The forest is full of animals.", "Orman hayvanlarla dolu.", "A2", "Nature", "https://images.unsplash.com/photo-1448375240586-882707db888b?w=300"),
        ("beach", "The sandy area beside the sea", "plaj/kumsal", "We spent the day at the beach.", "Günü plajda geçirdik.", "A2", "Nature", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300"),

        # Shopping & Money
        ("expensive", "Costing a lot of money", "pahalı", "This jacket is too expensive.", "Bu ceket çok pahalı.", "A2", "Shopping", None),
        ("cheap", "Not costing much money", "ucuz", "I found a cheap flight to London.", "Londra'ya ucuz bir uçuş buldum.", "A2", "Shopping", None),
        ("discount", "A reduction in price", "indirim", "There's a 20% discount today.", "Bugün %20 indirim var.", "A2", "Shopping", None),
        ("receipt", "A written proof of payment", "fiş/makbuz", "Keep the receipt in case you want to return it.", "İade etmek istersen fişi sakla.", "A2", "Shopping", None),
        ("customer", "A person who buys things", "müşteri", "The customer asked for a refund.", "Müşteri para iadesi istedi.", "A2", "Shopping", None),

        # ── B1 - Intermediate ──
        # Society & Culture
        ("government", "The group that runs a country", "hükümet", "The government announced new policies.", "Hükümet yeni politikalar açıkladı.", "B1", "Society", None),
        ("economy", "The system of money and trade", "ekonomi", "The economy is growing slowly.", "Ekonomi yavaşça büyüyor.", "B1", "Society", None),
        ("culture", "The customs and beliefs of a group", "kültür", "Every country has its own culture.", "Her ülkenin kendine özgü kültürü var.", "B1", "Society", None),
        ("population", "The number of people in an area", "nüfus", "The population of the city is growing.", "Şehrin nüfusu artıyor.", "B1", "Society", None),
        ("democracy", "A system where people vote", "demokrasi", "Democracy gives power to the people.", "Demokrasi gücü halka verir.", "B1", "Society", None),
        ("environment", "The natural world around us", "çevre", "We must protect the environment.", "Çevreyi korumalıyız.", "B1", "Society", "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=300"),
        ("pollution", "Harmful substances in the environment", "kirlilik", "Air pollution is a serious problem.", "Hava kirliliği ciddi bir sorundur.", "B1", "Society", None),
        ("freedom", "The right to act and speak freely", "özgürlük", "Freedom of speech is important.", "İfade özgürlüğü önemlidir.", "B1", "Society", None),

        # Emotions & Personality
        ("confident", "Feeling sure of yourself", "kendine güvenen", "She is a confident speaker.", "Kendine güvenen bir konuşmacı.", "B1", "Emotions", None),
        ("anxious", "Feeling worried or nervous", "endişeli/kaygılı", "I feel anxious before exams.", "Sınavlardan önce endişeli hissediyorum.", "B1", "Emotions", None),
        ("frustrated", "Feeling upset or annoyed", "sinirli/hayal kırıklığına uğramış", "He was frustrated with the slow internet.", "Yavaş internet yüzünden sinirlenmiş.", "B1", "Emotions", None),
        ("grateful", "Feeling thankful", "minnettar", "I am grateful for your help.", "Yardımınız için minnettarım.", "B1", "Emotions", None),
        ("ambitious", "Having a strong desire to succeed", "hırslı/azimli", "She is very ambitious and hardworking.", "Çok hırslı ve çalışkan.", "B1", "Personality", None),
        ("reliable", "Can be trusted and depended on", "güvenilir", "He is a reliable friend.", "Güvenilir bir arkadaştır.", "B1", "Personality", None),
        ("stubborn", "Refusing to change one's mind", "inatçı", "He's too stubborn to ask for help.", "Yardım istemek için çok inatçı.", "B1", "Personality", None),
        ("generous", "Willing to give and share", "cömert", "She is generous with her time.", "Zamanını cömertçe paylaşır.", "B1", "Personality", None),
        ("sensitive", "Easily affected by emotions", "hassas/duyarlı", "He is sensitive about criticism.", "Eleştiriye karşı hassastır.", "B1", "Personality", None),
        ("patient", "Able to wait calmly", "sabırlı", "Good teachers are patient.", "İyi öğretmenler sabırlıdır.", "B1", "Personality", None),

        # Technology
        ("software", "Computer programs", "yazılım", "We need to update the software.", "Yazılımı güncellememiz gerekiyor.", "B1", "Technology", None),
        ("hardware", "Physical parts of a computer", "donanım", "The hardware needs to be replaced.", "Donanımın değiştirilmesi gerekiyor.", "B1", "Technology", None),
        ("database", "An organized collection of data", "veritabanı", "All customer info is in the database.", "Tüm müşteri bilgileri veritabanında.", "B1", "Technology", None),
        ("website", "A set of pages on the internet", "web sitesi", "I found the information on their website.", "Bilgiyi web sitelerinde buldum.", "B1", "Technology", None),
        ("download", "To copy data from the internet", "indirmek", "You can download the app for free.", "Uygulamayı ücretsiz indirebilirsiniz.", "B1", "Technology", None),
        ("network", "A group of connected computers", "ağ", "The network connection is slow.", "Ağ bağlantısı yavaş.", "B1", "Technology", None),
        ("password", "A secret word for access", "şifre/parola", "Change your password regularly.", "Şifrenizi düzenli olarak değiştirin.", "B1", "Technology", None),
        ("artificial intelligence", "Computer systems that mimic human intelligence", "yapay zeka", "Artificial intelligence is changing many industries.", "Yapay zeka birçok sektörü değiştiriyor.", "B1", "Technology", None),

        # Business
        ("negotiate", "To discuss to reach an agreement", "müzakere etmek", "They negotiated a better price.", "Daha iyi bir fiyat için müzakere ettiler.", "B1", "Business", None),
        ("profit", "Money gained from business", "kâr", "The company made a big profit.", "Şirket büyük kâr elde etti.", "B1", "Business", None),
        ("investment", "Money put into something for profit", "yatırım", "Real estate is a good investment.", "Gayrimenkul iyi bir yatırımdır.", "B1", "Business", None),
        ("deadline", "The time by which something must be done", "son tarih/teslim tarihi", "The deadline for the project is Friday.", "Projenin son teslim tarihi Cuma.", "B1", "Business", None),
        ("colleague", "A person you work with", "iş arkadaşı/meslektaş", "I had lunch with my colleague.", "İş arkadaşımla öğle yemeği yedim.", "B1", "Business", None),
        ("contract", "A legal agreement", "sözleşme", "She signed a two-year contract.", "İki yıllık bir sözleşme imzaladı.", "B1", "Business", None),

        # ── B2 - Upper Intermediate ──
        # Academic
        ("hypothesis", "A proposed explanation for something", "hipotez/varsayım", "The scientist tested her hypothesis.", "Bilim insanı hipotezini test etti.", "B2", "Academic", None),
        ("methodology", "A system of methods used", "metodoloji/yöntem", "The research methodology was sound.", "Araştırma metodolojisi sağlamdı.", "B2", "Academic", None),
        ("phenomenon", "A fact or event that can be observed", "fenomen/olgu", "Global warming is a well-known phenomenon.", "Küresel ısınma bilinen bir olgudur.", "B2", "Academic", None),
        ("perspective", "A particular way of viewing things", "bakış açısı", "Try to see it from a different perspective.", "Farklı bir bakış açısından bakmayı dene.", "B2", "Academic", None),
        ("significant", "Important or notable", "önemli/kayda değer", "There was a significant improvement.", "Kayda değer bir gelişme oldu.", "B2", "Academic", None),
        ("comprehensive", "Including everything necessary", "kapsamlı", "The report provides a comprehensive overview.", "Rapor kapsamlı bir genel bakış sunuyor.", "B2", "Academic", None),
        ("controversial", "Causing disagreement", "tartışmalı", "The decision was controversial.", "Karar tartışmalıydı.", "B2", "Academic", None),
        ("fundamental", "Forming a base; essential", "temel", "Freedom is a fundamental right.", "Özgürlük temel bir haktır.", "B2", "Academic", None),
        ("contemporary", "Belonging to the present time", "çağdaş/günümüze ait", "Contemporary art is very diverse.", "Çağdaş sanat çok çeşitlidir.", "B2", "Academic", None),
        ("equivalent", "Equal in value or meaning", "eşdeğer", "One mile is equivalent to 1.6 kilometers.", "Bir mil 1.6 kilometreye eşdeğerdir.", "B2", "Academic", None),

        # Advanced Emotions
        ("overwhelmed", "Feeling too much at once", "bunalmış", "She felt overwhelmed by the workload.", "İş yükü karşısında bunalmış hissetti.", "B2", "Emotions", None),
        ("nostalgic", "Longing for the past", "nostaljik", "The song made me feel nostalgic.", "Şarkı beni nostaljik hissettirdi.", "B2", "Emotions", None),
        ("indifferent", "Having no interest or concern", "kayıtsız/ilgisiz", "He seemed indifferent to the news.", "Haberlere kayıtsız görünüyordu.", "B2", "Emotions", None),
        ("compassionate", "Feeling sympathy and concern", "şefkatli/merhametli", "She is a compassionate person.", "Şefkatli bir insandır.", "B2", "Emotions", None),
        ("resentful", "Feeling bitter about unfair treatment", "kırgın/gücenmiş", "He was resentful about being passed over.", "Göz ardı edildiği için kırgındı.", "B2", "Emotions", None),

        # Media & Communication
        ("broadcast", "To transmit by radio or TV", "yayınlamak", "The event was broadcast live.", "Etkinlik canlı yayınlandı.", "B2", "Media", None),
        ("journalism", "The work of reporting news", "gazetecilik", "She studied journalism at university.", "Üniversitede gazetecilik okudu.", "B2", "Media", None),
        ("propaganda", "Biased information to promote a cause", "propaganda", "The regime used propaganda to control people.", "Rejim insanları kontrol etmek için propaganda kullandı.", "B2", "Media", None),
        ("censorship", "The suppression of information", "sansür", "Censorship limits freedom of expression.", "Sansür ifade özgürlüğünü kısıtlar.", "B2", "Media", None),
        ("bias", "An unfair preference for or against", "önyargı/taraf tutma", "The article showed a clear bias.", "Makale açık bir önyargı gösterdi.", "B2", "Media", None),
        ("headline", "The title of a news article", "manşet/başlık", "The headline caught everyone's attention.", "Manşet herkesin dikkatini çekti.", "B2", "Media", None),

        # Law & Politics
        ("legislation", "A law or set of laws", "mevzuat/yasama", "New legislation was passed to protect workers.", "İşçileri korumak için yeni mevzuat çıkarıldı.", "B2", "Law", None),
        ("verdict", "A decision in a court case", "karar/hüküm", "The jury reached a verdict.", "Jüri bir karara vardı.", "B2", "Law", None),
        ("treaty", "A formal agreement between countries", "antlaşma", "Both nations signed the peace treaty.", "Her iki ülke barış antlaşmasını imzaladı.", "B2", "Law", None),
        ("amendment", "A change or addition to a law", "değişiklik/düzeltme", "The amendment was approved by parliament.", "Değişiklik parlamento tarafından onaylandı.", "B2", "Law", None),
        ("bureaucracy", "A system with many rules and procedures", "bürokrasi", "Bureaucracy slows down decision-making.", "Bürokrasi karar almayı yavaşlatır.", "B2", "Law", None),
        ("sovereignty", "Supreme power or authority", "egemenlik", "The country declared its sovereignty.", "Ülke egemenliğini ilan etti.", "B2", "Law", None),

        # Science & Environment
        ("ecosystem", "A community of living organisms", "ekosistem", "Coral reefs are fragile ecosystems.", "Mercan resifleri kırılgan ekosistemlerdir.", "B2", "Science", None),
        ("sustainability", "Meeting needs without harming the future", "sürdürülebilirlik", "Sustainability is key to our survival.", "Sürdürülebilirlik hayatta kalmamızın anahtarı.", "B2", "Science", None),
        ("biodiversity", "The variety of life in an area", "biyoçeşitlilik", "Biodiversity is declining rapidly.", "Biyoçeşitlilik hızla azalıyor.", "B2", "Science", None),
        ("carbon footprint", "The amount of CO2 produced", "karbon ayak izi", "We should reduce our carbon footprint.", "Karbon ayak izimizi azaltmalıyız.", "B2", "Science", None),
        ("renewable", "Able to be replenished naturally", "yenilenebilir", "Solar power is a renewable energy source.", "Güneş enerjisi yenilenebilir bir enerji kaynağıdır.", "B2", "Science", None),
        ("deforestation", "The clearing of forests", "ormansızlaşma", "Deforestation is destroying habitats.", "Ormansızlaşma yaşam alanlarını yok ediyor.", "B2", "Science", None),
    ]

    for word, meaning, translation, example, example_tr, level, category, image_url in vocabulary_data:
        cursor.execute(
            'INSERT INTO vocabulary (word, meaning, translation, example_sentence, example_translation, level, category, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (word, meaning, translation, example, example_tr, level, category, image_url)
        )

    # ═══════════════════════════════════════════
    # GRAMMAR LESSONS
    # ═══════════════════════════════════════════

    grammar_data = [
        # A1
        ("Present Simple - To Be", "A1",
         "The verb 'to be' is one of the most important verbs in English. It has three forms in the present: <strong>am, is, are</strong>.<br><br>"
         "<strong>I am</strong> (I'm)<br><strong>You are</strong> (You're)<br><strong>He/She/It is</strong> (He's/She's/It's)<br>"
         "<strong>We are</strong> (We're)<br><strong>They are</strong> (They're)<br><br>"
         "For negatives, add <strong>not</strong>: I am not, He is not (isn't), They are not (aren't).<br>"
         "For questions, put the verb first: <strong>Are you a student? Is she happy?</strong>",
         "I <strong>am</strong> a student.|She <strong>is</strong> happy.|They <strong>are</strong> from Turkey.|<strong>Are</strong> you ready?|He <strong>is not</strong> tired.", 1),

        ("Present Simple - Regular Verbs", "A1",
         "We use the <strong>Present Simple</strong> to talk about habits, routines, and general truths.<br><br>"
         "<strong>Form:</strong> Subject + base verb (add -s/-es for he/she/it)<br>"
         "<strong>I play</strong> tennis. / <strong>She plays</strong> tennis.<br>"
         "<strong>I go</strong> to school. / <strong>He goes</strong> to school.<br><br>"
         "<strong>Negative:</strong> Subject + do/does + not + base verb<br>"
         "I <strong>don't like</strong> coffee. / She <strong>doesn't like</strong> coffee.<br><br>"
         "<strong>Question:</strong> Do/Does + subject + base verb?<br>"
         "<strong>Do you speak</strong> English? / <strong>Does he play</strong> football?",
         "I <strong>go</strong> to school every day.|She <strong>speaks</strong> three languages.|We <strong>don't eat</strong> meat.|<strong>Does</strong> he <strong>like</strong> music?", 2),

        ("Articles: A, An, The", "A1",
         "<strong>A</strong> and <strong>An</strong> are indefinite articles. Use them with singular countable nouns when mentioning something for the first time.<br><br>"
         "<strong>A</strong> → before consonant sounds: a book, a cat, a university<br>"
         "<strong>An</strong> → before vowel sounds: an apple, an egg, an hour<br><br>"
         "<strong>The</strong> is the definite article. Use it when the listener knows which specific thing you mean.<br><br>"
         "I saw <strong>a</strong> dog. <strong>The</strong> dog was big. (First mention = a, second mention = the)",
         "I have <strong>a</strong> cat.|She ate <strong>an</strong> apple.|<strong>The</strong> sun is bright.|He is <strong>a</strong> teacher.", 3),

        ("Possessive Adjectives", "A1",
         "Possessive adjectives show who something belongs to.<br><br>"
         "<strong>my</strong> (I) → my book<br><strong>your</strong> (you) → your pen<br>"
         "<strong>his</strong> (he) → his car<br><strong>her</strong> (she) → her bag<br>"
         "<strong>its</strong> (it) → its tail<br><strong>our</strong> (we) → our house<br>"
         "<strong>their</strong> (they) → their school<br><br>"
         "They come before a noun: <strong>This is my phone.</strong>",
         "<strong>My</strong> name is John.|<strong>Her</strong> cat is cute.|<strong>Their</strong> house is big.|Is this <strong>your</strong> bag?", 4),

        ("There is / There are", "A1",
         "Use <strong>there is</strong> with singular nouns and <strong>there are</strong> with plural nouns to say something exists.<br><br>"
         "<strong>There is</strong> a book on the table.<br>"
         "<strong>There are</strong> three cats in the garden.<br><br>"
         "<strong>Negative:</strong> There isn't / There aren't<br>"
         "<strong>Question:</strong> Is there...? / Are there...?",
         "<strong>There is</strong> a park near my house.|<strong>There are</strong> many students in the class.|<strong>Is there</strong> a bank nearby?|<strong>There aren't</strong> any eggs.", 5),

        # A2
        ("Past Simple", "A2",
         "We use the <strong>Past Simple</strong> to talk about completed actions in the past.<br><br>"
         "<strong>Regular verbs:</strong> Add -ed (worked, played, studied)<br>"
         "<strong>Irregular verbs:</strong> Special forms (go→went, eat→ate, see→saw)<br><br>"
         "<strong>Negative:</strong> didn't + base verb → I <strong>didn't go</strong> to school.<br>"
         "<strong>Question:</strong> Did + subject + base verb? → <strong>Did you see</strong> the movie?<br><br>"
         "<strong>Time expressions:</strong> yesterday, last week, two days ago, in 2020",
         "I <strong>visited</strong> my grandmother yesterday.|She <strong>went</strong> to Paris last summer.|They <strong>didn't watch</strong> the movie.|<strong>Did</strong> you <strong>finish</strong> your homework?", 1),

        ("Present Continuous", "A2",
         "We use the <strong>Present Continuous</strong> to talk about actions happening right now or temporary situations.<br><br>"
         "<strong>Form:</strong> Subject + am/is/are + verb-ing<br>"
         "I <strong>am studying</strong> English.<br>She <strong>is reading</strong> a book.<br>They <strong>are playing</strong> football.<br><br>"
         "<strong>Negative:</strong> Subject + am/is/are + not + verb-ing<br>"
         "I <strong>am not working</strong> today.<br><br>"
         "<strong>Question:</strong> Am/Is/Are + subject + verb-ing?<br>"
         "<strong>Are you listening</strong> to me?",
         "I <strong>am reading</strong> a book right now.|She <strong>is cooking</strong> dinner.|They <strong>are not playing</strong> outside.|<strong>Is</strong> he <strong>sleeping</strong>?", 2),

        ("Comparatives and Superlatives", "A2",
         "<strong>Comparatives</strong> compare two things. <strong>Superlatives</strong> compare three or more things.<br><br>"
         "<strong>Short adjectives:</strong><br>"
         "tall → tall<strong>er</strong> → the tall<strong>est</strong><br>"
         "big → bigg<strong>er</strong> → the bigg<strong>est</strong><br><br>"
         "<strong>Long adjectives:</strong><br>"
         "beautiful → <strong>more</strong> beautiful → <strong>the most</strong> beautiful<br><br>"
         "<strong>Irregular:</strong><br>"
         "good → better → the best<br>bad → worse → the worst",
         "She is <strong>taller than</strong> her brother.|This is <strong>the best</strong> restaurant in town.|English is <strong>easier than</strong> Chinese.|He is <strong>the most intelligent</strong> student.", 3),

        ("Modal Verbs: Can, Must, Should", "A2",
         "<strong>Can</strong> → ability or permission<br>"
         "I <strong>can</strong> swim. / <strong>Can</strong> I go home?<br><br>"
         "<strong>Must</strong> → obligation or necessity<br>"
         "You <strong>must</strong> wear a seatbelt. / You <strong>must not</strong> smoke here.<br><br>"
         "<strong>Should</strong> → advice or recommendation<br>"
         "You <strong>should</strong> study more. / You <strong>shouldn't</strong> eat too much sugar.<br><br>"
         "These verbs don't change form: He <strong>can</strong> swim (NOT he cans).",
         "She <strong>can</strong> speak French.|You <strong>must</strong> finish your homework.|You <strong>should</strong> see a doctor.|He <strong>can't</strong> drive yet.", 4),

        ("Prepositions of Time and Place", "A2",
         "<strong>Prepositions of Time:</strong><br>"
         "<strong>at</strong> → specific time: at 5 PM, at night<br>"
         "<strong>on</strong> → days/dates: on Monday, on January 1st<br>"
         "<strong>in</strong> → months/years/seasons: in March, in 2024, in summer<br><br>"
         "<strong>Prepositions of Place:</strong><br>"
         "<strong>at</strong> → specific point: at the bus stop, at home<br>"
         "<strong>on</strong> → surface: on the table, on the wall<br>"
         "<strong>in</strong> → enclosed space: in the room, in the box",
         "The meeting is <strong>at</strong> 3 PM.|I was born <strong>in</strong> June.|The book is <strong>on</strong> the table.|She is <strong>at</strong> the airport.", 5),

        # B1
        ("Present Perfect", "B1",
         "We use the <strong>Present Perfect</strong> to talk about past actions with a connection to the present.<br><br>"
         "<strong>Form:</strong> Subject + have/has + past participle<br>"
         "I <strong>have visited</strong> London three times.<br>She <strong>has finished</strong> her work.<br><br>"
         "<strong>Key words:</strong> already, yet, just, ever, never, since, for<br>"
         "I have <strong>already</strong> eaten. / She <strong>hasn't</strong> arrived <strong>yet</strong>.<br>"
         "Have you <strong>ever</strong> been to Japan? / I have <strong>never</strong> seen snow.<br><br>"
         "<strong>since</strong> → a specific point: since 2020, since Monday<br>"
         "<strong>for</strong> → a period: for three years, for a long time",
         "I <strong>have lived</strong> here <strong>for</strong> ten years.|She <strong>has just finished</strong> her homework.|<strong>Have</strong> you <strong>ever been</strong> to London?|They <strong>haven't decided</strong> yet.", 1),

        ("Conditionals: First & Second", "B1",
         "<strong>First Conditional</strong> (real/possible future):<br>"
         "If + present simple, will + base verb<br>"
         "If it <strong>rains</strong>, I <strong>will stay</strong> home.<br>"
         "If you <strong>study</strong> hard, you <strong>will pass</strong> the exam.<br><br>"
         "<strong>Second Conditional</strong> (unreal/hypothetical):<br>"
         "If + past simple, would + base verb<br>"
         "If I <strong>had</strong> a million dollars, I <strong>would travel</strong> the world.<br>"
         "If she <strong>were</strong> taller, she <strong>would play</strong> basketball.",
         "If I <strong>have</strong> time, I <strong>will call</strong> you.|If I <strong>were</strong> you, I <strong>would accept</strong> the offer.|If it <strong>rains</strong>, we <strong>will cancel</strong> the picnic.|If she <strong>studied</strong> harder, she <strong>would get</strong> better grades.", 2),

        ("Passive Voice", "B1",
         "We use the <strong>Passive Voice</strong> when the action is more important than who does it, or when we don't know who did it.<br><br>"
         "<strong>Form:</strong> Subject + be + past participle (+ by agent)<br><br>"
         "<strong>Present:</strong> The car <strong>is washed</strong> every week.<br>"
         "<strong>Past:</strong> The letter <strong>was written</strong> by John.<br>"
         "<strong>Future:</strong> The project <strong>will be completed</strong> next month.<br>"
         "<strong>Present Perfect:</strong> The book <strong>has been translated</strong> into 20 languages.",
         "English <strong>is spoken</strong> all over the world.|The Mona Lisa <strong>was painted</strong> by Leonardo da Vinci.|The new school <strong>will be built</strong> next year.|The email <strong>has been sent</strong>.", 3),

        ("Relative Clauses", "B1",
         "<strong>Relative clauses</strong> give extra information about a noun using relative pronouns.<br><br>"
         "<strong>who</strong> → for people: The man <strong>who</strong> lives next door is a doctor.<br>"
         "<strong>which</strong> → for things: The book <strong>which</strong> I read was great.<br>"
         "<strong>that</strong> → for people or things: The car <strong>that</strong> I bought is red.<br>"
         "<strong>where</strong> → for places: The city <strong>where</strong> I was born is small.<br>"
         "<strong>whose</strong> → for possession: The woman <strong>whose</strong> bag was stolen called the police.",
         "The teacher <strong>who</strong> taught me was kind.|This is the book <strong>which</strong> won the prize.|The restaurant <strong>where</strong> we ate was excellent.|The man <strong>whose</strong> car broke down needed help.", 4),

        ("Reported Speech", "B1",
         "<strong>Reported (Indirect) Speech</strong> tells what someone said without using their exact words.<br><br>"
         "<strong>Rules:</strong> Change tense one step back, change pronouns and time expressions.<br><br>"
         "Direct: 'I <strong>am</strong> happy.' → Reported: She said she <strong>was</strong> happy.<br>"
         "Direct: 'I <strong>will come</strong>.' → Reported: He said he <strong>would come</strong>.<br>"
         "Direct: 'I <strong>can swim</strong>.' → Reported: She said she <strong>could swim</strong>.<br><br>"
         "<strong>Questions:</strong> He asked <strong>if/whether</strong> I liked coffee. (yes/no)<br>"
         "She asked <strong>where</strong> I lived. (wh-question)",
         "She said she <strong>was</strong> tired.|He told me he <strong>would help</strong>.|They said they <strong>had finished</strong>.|She asked if I <strong>could come</strong>.", 5),

        # B2
        ("Third Conditional", "B2",
         "The <strong>Third Conditional</strong> talks about unreal past situations and their imagined results.<br><br>"
         "<strong>Form:</strong> If + past perfect, would have + past participle<br><br>"
         "If I <strong>had studied</strong> harder, I <strong>would have passed</strong> the exam.<br>"
         "If she <strong>had left</strong> earlier, she <strong>wouldn't have missed</strong> the train.<br><br>"
         "We use it to express regret or imagine different outcomes for past events.",
         "If I <strong>had known</strong>, I <strong>would have helped</strong>.|If they <strong>had arrived</strong> on time, they <strong>would have seen</strong> the show.|She <strong>wouldn't have failed</strong> if she <strong>had prepared</strong>.", 1),

        ("Advanced Passive Constructions", "B2",
         "Beyond basic passives, English has several advanced passive forms:<br><br>"
         "<strong>Passive with modals:</strong> The work <strong>must be finished</strong> by Friday.<br>"
         "<strong>Passive with get:</strong> He <strong>got fired</strong> last week. (informal)<br>"
         "<strong>Have/Get something done:</strong> I <strong>had my car repaired</strong>. (someone did it for me)<br>"
         "<strong>Impersonal passive:</strong> It <strong>is believed</strong> that... / He <strong>is said to be</strong> rich.<br>"
         "<strong>Passive infinitive:</strong> She wants <strong>to be promoted</strong>.",
         "The report <strong>should be submitted</strong> tomorrow.|I need to <strong>get my hair cut</strong>.|It <strong>is thought</strong> that the economy will recover.|She <strong>had her phone stolen</strong>.", 2),

        ("Subjunctive and Wish Clauses", "B2",
         "We use <strong>wish</strong> + past tense to express desires about present situations.<br>"
         "I <strong>wish I had</strong> more free time. (but I don't)<br><br>"
         "<strong>Wish + past perfect</strong> for regrets about the past:<br>"
         "I <strong>wish I had studied</strong> medicine. (but I didn't)<br><br>"
         "<strong>Wish + would</strong> for things we want to change:<br>"
         "I <strong>wish you would stop</strong> making noise.<br><br>"
         "<strong>Subjunctive</strong> after certain expressions:<br>"
         "It's important <strong>that he be</strong> on time. / I suggest <strong>that she study</strong> more.",
         "I <strong>wish I could</strong> fly.|She <strong>wishes she had</strong> accepted the job.|I <strong>wish</strong> it <strong>would stop</strong> raining.|They suggested he <strong>arrive</strong> early.", 3),

        ("Inversion for Emphasis", "B2",
         "<strong>Inversion</strong> places the auxiliary before the subject for emphasis or formal style.<br><br>"
         "<strong>Negative adverbials:</strong><br>"
         "<strong>Never have</strong> I seen such beauty.<br>"
         "<strong>Rarely does</strong> he arrive on time.<br>"
         "<strong>Not only did</strong> she win, <strong>but</strong> she also broke the record.<br><br>"
         "<strong>Other patterns:</strong><br>"
         "<strong>Had I known</strong>, I would have come. (= If I had known)<br>"
         "<strong>Were she</strong> here, she would help. (= If she were here)",
         "<strong>Never have</strong> I been so surprised.|<strong>Not only</strong> is she smart, <strong>but also</strong> kind.|<strong>Had</strong> they arrived earlier, they <strong>would have</strong> found seats.|<strong>Seldom do</strong> we see such talent.", 4),

        ("Discourse Markers & Linking Words", "B2",
         "Advanced linking words help organize ideas and arguments:<br><br>"
         "<strong>Adding:</strong> furthermore, moreover, in addition, besides<br>"
         "<strong>Contrasting:</strong> however, nevertheless, on the other hand, whereas<br>"
         "<strong>Cause/Effect:</strong> consequently, therefore, as a result, due to<br>"
         "<strong>Giving examples:</strong> for instance, such as, namely<br>"
         "<strong>Summarizing:</strong> in conclusion, to sum up, overall<br>"
         "<strong>Sequencing:</strong> firstly, subsequently, finally",
         "The project was difficult; <strong>however</strong>, we finished on time.|<strong>Furthermore</strong>, the results exceeded expectations.|<strong>Consequently</strong>, the company decided to expand.|<strong>In conclusion</strong>, education is the key to success.", 5),
    ]

    for title, level, explanation, examples, order_num in grammar_data:
        cursor.execute(
            'INSERT INTO grammar_lessons (title, level, explanation, examples, order_num) VALUES (?, ?, ?, ?, ?)',
            (title, level, explanation, examples, order_num)
        )

    # ═══════════════════════════════════════════
    # QUIZZES - Multiple types per level
    # ═══════════════════════════════════════════

    quiz_data = [
        # A1 Quizzes
        ("She ___ a student.", "fill_blank", None, "is", "A1", "grammar", None),
        ("They ___ from Turkey.", "fill_blank", None, "are", "A1", "grammar", None),
        ("I ___ not happy today.", "fill_blank", None, "am", "A1", "grammar", None),
        ("What is the meaning of 'apple'?", "multiple_choice", json.dumps(["A fruit", "A vegetable", "A drink", "A color"]), "A fruit", "A1", "vocabulary", None),
        ("What is the meaning of 'mother'?", "multiple_choice", json.dumps(["A male parent", "A female parent", "A sibling", "A friend"]), "A female parent", "A1", "vocabulary", None),
        ("Which is correct?", "multiple_choice", json.dumps(["She have a cat.", "She has a cat.", "She haves a cat.", "She having a cat."]), "She has a cat.", "A1", "grammar", None),
        ("Fix this sentence: 'He are a teacher.'", "sentence_correction", None, "He is a teacher.", "A1", "grammar", None),
        ("Fix this sentence: 'I has two brothers.'", "sentence_correction", None, "I have two brothers.", "A1", "grammar", None),
        ("I go to school ___ day.", "fill_blank", None, "every", "A1", "grammar", None),
        ("___ you like pizza?", "fill_blank", None, "Do", "A1", "grammar", None),
        ("She ___ (play) tennis on Saturdays.", "fill_blank", None, "plays", "A1", "grammar", None),
        ("This is ___ apple.", "multiple_choice", json.dumps(["a", "an", "the", "—"]), "an", "A1", "grammar", None),
        ("___ is a book on the table.", "fill_blank", None, "There", "A1", "grammar", None),
        ("What is the opposite of 'hello'?", "multiple_choice", json.dumps(["Please", "Goodbye", "Sorry", "Thank you"]), "Goodbye", "A1", "vocabulary", None),
        ("My ___ (mother) name is Sarah.", "fill_blank", None, "mother's", "A1", "grammar", None),

        # A2 Quizzes
        ("I ___ (go) to London last summer.", "fill_blank", None, "went", "A2", "grammar", None),
        ("She ___ (not/see) the movie yesterday.", "fill_blank", None, "didn't see", "A2", "grammar", None),
        ("Which is correct?", "multiple_choice", json.dumps(["She is more tall than me.", "She is taller than me.", "She is more taller than me.", "She is tallest than me."]), "She is taller than me.", "A2", "grammar", None),
        ("You ___ wear a helmet when riding a bike.", "multiple_choice", json.dumps(["can", "should", "would", "shall"]), "should", "A2", "grammar", None),
        ("The meeting is ___ Monday.", "multiple_choice", json.dumps(["in", "at", "on", "to"]), "on", "A2", "grammar", None),
        ("I was born ___ 1998.", "fill_blank", None, "in", "A2", "grammar", None),
        ("She ___ (cook) dinner right now.", "fill_blank", None, "is cooking", "A2", "grammar", None),
        ("Fix this sentence: 'He goed to the store.'", "sentence_correction", None, "He went to the store.", "A2", "grammar", None),
        ("Fix this sentence: 'She is more beautiful that her sister.'", "sentence_correction", None, "She is more beautiful than her sister.", "A2", "grammar", None),
        ("This is the ___ (good) restaurant in town.", "fill_blank", None, "best", "A2", "grammar", None),
        ("What does 'luggage' mean?", "multiple_choice", json.dumps(["A type of food", "Bags for traveling", "A vehicle", "A document"]), "Bags for traveling", "A2", "vocabulary", None),
        ("You ___ not park here.", "multiple_choice", json.dumps(["can", "must", "should", "would"]), "must", "A2", "grammar", None),
        ("What is a 'discount'?", "multiple_choice", json.dumps(["An extra charge", "A type of payment", "A reduction in price", "A receipt"]), "A reduction in price", "A2", "vocabulary", None),
        ("___ you ever been to Japan?", "fill_blank", None, "Have", "A2", "grammar", None),
        ("She ___ (study) when I called.", "fill_blank", None, "was studying", "A2", "grammar", None),

        # B1 Quizzes
        ("I ___ (live) here since 2010.", "fill_blank", None, "have lived", "B1", "grammar", None),
        ("If it rains, I ___ (stay) home.", "fill_blank", None, "will stay", "B1", "grammar", None),
        ("If I ___ (be) rich, I would travel the world.", "fill_blank", None, "were", "B1", "grammar", None),
        ("English ___ (speak) all over the world.", "fill_blank", None, "is spoken", "B1", "grammar", None),
        ("The man ___ lives next door is a doctor.", "multiple_choice", json.dumps(["which", "who", "where", "whose"]), "who", "B1", "grammar", None),
        ("She said she ___ tired.", "multiple_choice", json.dumps(["is", "was", "were", "be"]), "was", "B1", "grammar", None),
        ("Fix this sentence: 'If I would have money, I would buy a car.'", "sentence_correction", None, "If I had money, I would buy a car.", "B1", "grammar", None),
        ("Fix this sentence: 'The book who I read was great.'", "sentence_correction", None, "The book which I read was great.", "B1", "grammar", None),
        ("She has worked here ___ five years.", "multiple_choice", json.dumps(["since", "for", "ago", "from"]), "for", "B1", "grammar", None),
        ("He told me that he ___ come tomorrow.", "fill_blank", None, "would", "B1", "grammar", None),
        ("What does 'negotiate' mean?", "multiple_choice", json.dumps(["To argue", "To discuss to reach agreement", "To refuse", "To accept"]), "To discuss to reach agreement", "B1", "vocabulary", None),
        ("What does 'ambitious' mean?", "multiple_choice", json.dumps(["Lazy", "Having a strong desire to succeed", "Being afraid", "Being careful"]), "Having a strong desire to succeed", "B1", "vocabulary", None),
        ("The letter ___ (write) by John yesterday.", "fill_blank", None, "was written", "B1", "grammar", None),
        ("I wish I ___ (know) the answer.", "fill_blank", None, "knew", "B1", "grammar", None),
        ("The city ___ I was born is small.", "multiple_choice", json.dumps(["who", "which", "where", "that"]), "where", "B1", "grammar", None),

        # B2 Quizzes
        ("If I ___ (study) harder, I would have passed.", "fill_blank", None, "had studied", "B2", "grammar", None),
        ("Never ___ I seen such beauty.", "fill_blank", None, "have", "B2", "grammar", None),
        ("Not only ___ she smart, but also kind.", "fill_blank", None, "is", "B2", "grammar", None),
        ("I wish I ___ (accept) that job offer.", "fill_blank", None, "had accepted", "B2", "grammar", None),
        ("It ___ (believe) that the economy will recover.", "fill_blank", None, "is believed", "B2", "grammar", None),
        ("Which linking word means 'as a result'?", "multiple_choice", json.dumps(["However", "Consequently", "Moreover", "Besides"]), "Consequently", "B2", "grammar", None),
        ("Fix this sentence: 'Had I knew about it, I would have come.'", "sentence_correction", None, "Had I known about it, I would have come.", "B2", "grammar", None),
        ("Fix this sentence: 'Not only she is smart, but also kind.'", "sentence_correction", None, "Not only is she smart, but also kind.", "B2", "grammar", None),
        ("What does 'hypothesis' mean?", "multiple_choice", json.dumps(["A proven fact", "A proposed explanation", "A mathematical formula", "A type of experiment"]), "A proposed explanation", "B2", "vocabulary", None),
        ("What does 'sovereignty' mean?", "multiple_choice", json.dumps(["Poverty", "Freedom of speech", "Supreme power or authority", "A trade agreement"]), "Supreme power or authority", "B2", "vocabulary", None),
        ("I need to get my car ___ (repair).", "fill_blank", None, "repaired", "B2", "grammar", None),
        ("___ she here, she would help.", "fill_blank", None, "Were", "B2", "grammar", None),
        ("The project was difficult; ___, we finished on time.", "multiple_choice", json.dumps(["furthermore", "however", "moreover", "besides"]), "however", "B2", "grammar", None),
        ("She ___ (say) to be the best in her field.", "fill_blank", None, "is said", "B2", "grammar", None),
        ("What does 'sustainability' mean?", "multiple_choice", json.dumps(["Making a profit", "Meeting needs without harming the future", "Building more factories", "Reducing the population"]), "Meeting needs without harming the future", "B2", "vocabulary", None),
    ]

    for question, quiz_type, options, correct, level, category, lesson_id in quiz_data:
        cursor.execute(
            'INSERT INTO quizzes (question, quiz_type, options, correct_answer, level, category, lesson_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (question, quiz_type, options, correct, level, category, lesson_id)
        )

    # Now link some quizzes to grammar lessons
    lessons = cursor.execute('SELECT id, title, level FROM grammar_lessons').fetchall()
    lesson_map = {}
    for l in lessons:
        lesson_map[(l[2], l[0])] = l[0]

    # ═══════════════════════════════════════════
    # PLACEMENT TEST QUESTIONS
    # ═══════════════════════════════════════════

    placement_data = [
        # Easy (A1)
        ("She ___ a teacher.", json.dumps(["am", "is", "are", "be"]), "is", "A1"),
        ("I ___ from Turkey.", json.dumps(["am", "is", "are", "be"]), "am", "A1"),
        ("They ___ students.", json.dumps(["am", "is", "are", "be"]), "are", "A1"),
        ("He ___ to school every day.", json.dumps(["go", "goes", "going", "gone"]), "goes", "A1"),
        ("This is ___ orange.", json.dumps(["a", "an", "the", "—"]), "an", "A1"),

        # Medium-Easy (A2)
        ("I ___ to London last year.", json.dumps(["go", "goes", "went", "gone"]), "went", "A2"),
        ("She is ___ than her sister.", json.dumps(["tall", "taller", "tallest", "more tall"]), "taller", "A2"),
        ("You ___ smoke here. It's forbidden.", json.dumps(["must", "mustn't", "should", "can"]), "mustn't", "A2"),
        ("She ___ dinner right now.", json.dumps(["cooks", "cooked", "is cooking", "cook"]), "is cooking", "A2"),
        ("We arrived ___ the airport early.", json.dumps(["in", "at", "on", "to"]), "at", "A2"),

        # Medium (B1)
        ("I have lived here ___ 2015.", json.dumps(["for", "since", "ago", "from"]), "since", "B1"),
        ("If I had more money, I ___ a new car.", json.dumps(["buy", "bought", "would buy", "will buy"]), "would buy", "B1"),
        ("The book ___ by millions of people.", json.dumps(["reads", "is read", "read", "reading"]), "is read", "B1"),
        ("She told me she ___ tired.", json.dumps(["is", "was", "were", "be"]), "was", "B1"),
        ("The woman ___ car was stolen called police.", json.dumps(["who", "which", "whose", "that"]), "whose", "B1"),

        # Hard (B2)
        ("If I ___ earlier, I would have caught the train.", json.dumps(["leave", "left", "had left", "would leave"]), "had left", "B2"),
        ("Never ___ I experienced such kindness.", json.dumps(["did", "have", "was", "had"]), "have", "B2"),
        ("The report ___ by tomorrow.", json.dumps(["must finish", "must be finished", "must finishing", "must to finish"]), "must be finished", "B2"),
        ("I wish I ___ accepted that job.", json.dumps(["have", "had", "would", "did"]), "had", "B2"),
        ("___, the project was completed on time.", json.dumps(["However", "Nevertheless", "Moreover", "Consequently"]), "Nevertheless", "B2"),
    ]

    for question, options, correct, difficulty in placement_data:
        cursor.execute(
            'INSERT INTO placement_questions (question, options, correct_answer, difficulty) VALUES (?, ?, ?, ?)',
            (question, options, correct, difficulty)
        )

    # ═══════════════════════════════════════════
    # SPEAKING SCENARIOS
    # ═══════════════════════════════════════════

    speaking_data = [
        # A1
        ("Meeting Someone New", "Practice introducing yourself to a new person.", "A1",
         json.dumps([
             {"speaker": "You", "line": "Hello! My name is ___. What's your name?"},
             {"speaker": "Partner", "line": "Hi! I'm Sarah. Nice to meet you!"},
             {"speaker": "You", "line": "Nice to meet you too! Where are you from?"},
             {"speaker": "Partner", "line": "I'm from London. And you?"},
             {"speaker": "You", "line": "I'm from ___. I'm a student."},
             {"speaker": "Partner", "line": "That's great! What do you study?"},
             {"speaker": "You", "line": "I study ___. It's very interesting."},
             {"speaker": "Partner", "line": "Sounds nice! Good luck with your studies!"},
             {"speaker": "You", "line": "Thank you! See you later!"}
         ]), "Introduction"),

        ("Ordering Food", "Practice ordering food at a simple restaurant.", "A1",
         json.dumps([
             {"speaker": "Waiter", "line": "Welcome! What would you like to eat?"},
             {"speaker": "You", "line": "I would like a sandwich, please."},
             {"speaker": "Waiter", "line": "Would you like something to drink?"},
             {"speaker": "You", "line": "Yes, a glass of water, please."},
             {"speaker": "Waiter", "line": "Anything else?"},
             {"speaker": "You", "line": "No, thank you. How much is it?"},
             {"speaker": "Waiter", "line": "That's five dollars."},
             {"speaker": "You", "line": "Here you go. Thank you!"},
             {"speaker": "Waiter", "line": "Thank you! Enjoy your meal!"}
         ]), "Restaurant"),

        ("Asking for Directions", "Practice asking and understanding simple directions.", "A1",
         json.dumps([
             {"speaker": "You", "line": "Excuse me, where is the train station?"},
             {"speaker": "Stranger", "line": "Go straight and turn left at the traffic light."},
             {"speaker": "You", "line": "Turn left at the traffic light?"},
             {"speaker": "Stranger", "line": "Yes, then walk for about five minutes."},
             {"speaker": "You", "line": "Is it far from here?"},
             {"speaker": "Stranger", "line": "No, it's about a ten-minute walk."},
             {"speaker": "You", "line": "Thank you very much!"},
             {"speaker": "Stranger", "line": "You're welcome! Have a nice day!"}
         ]), "Directions"),

        # A2
        ("At the Doctor's Office", "Practice describing symptoms to a doctor.", "A2",
         json.dumps([
             {"speaker": "Doctor", "line": "Good morning. What seems to be the problem?"},
             {"speaker": "You", "line": "Good morning, doctor. I have a headache and a sore throat."},
             {"speaker": "Doctor", "line": "How long have you had these symptoms?"},
             {"speaker": "You", "line": "Since yesterday morning."},
             {"speaker": "Doctor", "line": "Do you have a fever?"},
             {"speaker": "You", "line": "Yes, I think so. I feel very hot."},
             {"speaker": "Doctor", "line": "Let me check. Yes, you have a slight fever. I'll prescribe some medicine."},
             {"speaker": "You", "line": "How often should I take the medicine?"},
             {"speaker": "Doctor", "line": "Take it three times a day after meals. Get plenty of rest."},
             {"speaker": "You", "line": "Thank you, doctor. When should I come back?"},
             {"speaker": "Doctor", "line": "Come back in three days if you don't feel better."}
         ]), "Health"),

        ("Shopping for Clothes", "Practice buying clothes at a shop.", "A2",
         json.dumps([
             {"speaker": "Shop Assistant", "line": "Can I help you?"},
             {"speaker": "You", "line": "Yes, I'm looking for a blue shirt."},
             {"speaker": "Shop Assistant", "line": "What size do you need?"},
             {"speaker": "You", "line": "Medium, please."},
             {"speaker": "Shop Assistant", "line": "Here you are. Would you like to try it on?"},
             {"speaker": "You", "line": "Yes, please. Where is the fitting room?"},
             {"speaker": "Shop Assistant", "line": "It's over there, on the right."},
             {"speaker": "You", "line": "Thank you. ... It fits well. How much is it?"},
             {"speaker": "Shop Assistant", "line": "It's 25 dollars. We also have a 10% discount today."},
             {"speaker": "You", "line": "Great! I'll take it. Can I pay by card?"},
             {"speaker": "Shop Assistant", "line": "Of course. Here's your receipt."}
         ]), "Shopping"),

        ("Making Plans with a Friend", "Practice making plans and arrangements.", "A2",
         json.dumps([
             {"speaker": "Friend", "line": "Hey! What are you doing this weekend?"},
             {"speaker": "You", "line": "I don't have any plans yet. Why?"},
             {"speaker": "Friend", "line": "Do you want to go to the cinema?"},
             {"speaker": "You", "line": "Sure! What movie do you want to see?"},
             {"speaker": "Friend", "line": "There's a new action movie. It starts at 7 PM."},
             {"speaker": "You", "line": "Sounds great! Where should we meet?"},
             {"speaker": "Friend", "line": "Let's meet at the cinema entrance at 6:45."},
             {"speaker": "You", "line": "Perfect! Do you want to have dinner before the movie?"},
             {"speaker": "Friend", "line": "That's a good idea! Let's meet at 5:30 then."},
             {"speaker": "You", "line": "OK, see you on Saturday at 5:30!"}
         ]), "Social"),

        # B1
        ("Job Interview", "Practice answering common job interview questions.", "B1",
         json.dumps([
             {"speaker": "Interviewer", "line": "Good morning. Please take a seat. Can you tell me about yourself?"},
             {"speaker": "You", "line": "Good morning. My name is ___. I graduated from ___ University with a degree in ___."},
             {"speaker": "Interviewer", "line": "What are your main strengths?"},
             {"speaker": "You", "line": "I'm a hard worker, I'm good at teamwork, and I can manage my time well."},
             {"speaker": "Interviewer", "line": "Why do you want to work for our company?"},
             {"speaker": "You", "line": "I've researched your company and I'm impressed by your innovative approach. I believe I can contribute to your team."},
             {"speaker": "Interviewer", "line": "Where do you see yourself in five years?"},
             {"speaker": "You", "line": "I hope to have developed my skills and taken on more responsibility within the company."},
             {"speaker": "Interviewer", "line": "Do you have any questions for us?"},
             {"speaker": "You", "line": "Yes, could you tell me more about the team I would be working with?"},
             {"speaker": "Interviewer", "line": "Of course. We have a team of about ten people. Thank you for coming in today."},
             {"speaker": "You", "line": "Thank you for the opportunity. I look forward to hearing from you."}
         ]), "Work"),

        ("Discussing Current Events", "Practice discussing news and current events.", "B1",
         json.dumps([
             {"speaker": "Friend", "line": "Did you see the news about climate change?"},
             {"speaker": "You", "line": "Yes, it's really concerning. The temperatures have been rising every year."},
             {"speaker": "Friend", "line": "I know. What do you think we should do about it?"},
             {"speaker": "You", "line": "I think we need to use more renewable energy and reduce our carbon footprint."},
             {"speaker": "Friend", "line": "That's true. Do you think governments are doing enough?"},
             {"speaker": "You", "line": "Not really. I believe they should invest more in green technology."},
             {"speaker": "Friend", "line": "I agree. What about individual actions?"},
             {"speaker": "You", "line": "Everyone can help by using public transport, recycling, and consuming less."},
             {"speaker": "Friend", "line": "You're right. Small changes can make a big difference."}
         ]), "Discussion"),

        ("Complaining at a Hotel", "Practice making a polite complaint.", "B1",
         json.dumps([
             {"speaker": "You", "line": "Excuse me, I'd like to speak to someone about my room."},
             {"speaker": "Receptionist", "line": "Of course. What seems to be the problem?"},
             {"speaker": "You", "line": "The air conditioning isn't working and the room is very hot."},
             {"speaker": "Receptionist", "line": "I'm sorry to hear that. When did you notice the problem?"},
             {"speaker": "You", "line": "Last night. I couldn't sleep because of the heat."},
             {"speaker": "Receptionist", "line": "I apologize for the inconvenience. I can move you to another room."},
             {"speaker": "You", "line": "That would be great. Could I also get a discount for last night?"},
             {"speaker": "Receptionist", "line": "Let me check with my manager. I'll do my best to help."},
             {"speaker": "You", "line": "Thank you. I appreciate your help."}
         ]), "Travel"),

        # B2
        ("Debating a Topic", "Practice presenting and defending an argument.", "B2",
         json.dumps([
             {"speaker": "Moderator", "line": "Today's topic: Should social media be regulated? What's your position?"},
             {"speaker": "You", "line": "I believe social media should be regulated to some extent, primarily to prevent the spread of misinformation."},
             {"speaker": "Opponent", "line": "But wouldn't regulation violate freedom of speech?"},
             {"speaker": "You", "line": "Not necessarily. We already have regulations against hate speech and defamation. Social media shouldn't be exempt."},
             {"speaker": "Opponent", "line": "Who would decide what constitutes misinformation?"},
             {"speaker": "You", "line": "Independent fact-checking organizations could be involved. Furthermore, transparency about algorithms would help users make informed decisions."},
             {"speaker": "Moderator", "line": "What about the economic impact?"},
             {"speaker": "You", "line": "Regulation doesn't have to stifle innovation. On the contrary, clear rules could create a healthier digital environment."},
             {"speaker": "Opponent", "line": "I see your point, but implementation would be challenging."},
             {"speaker": "You", "line": "Indeed, it would require international cooperation. Nevertheless, the potential benefits outweigh the challenges."}
         ]), "Debate"),

        ("Academic Presentation", "Practice giving a short academic presentation.", "B2",
         json.dumps([
             {"speaker": "You", "line": "Good morning, everyone. Today I'll be presenting my research on renewable energy sources."},
             {"speaker": "You", "line": "Firstly, let me give you an overview of the current energy landscape."},
             {"speaker": "You", "line": "According to recent studies, fossil fuels still account for approximately 80% of global energy consumption."},
             {"speaker": "You", "line": "However, renewable energy has been growing significantly. Solar power capacity has increased by 40% in the last five years."},
             {"speaker": "You", "line": "Moving on to the challenges, the main obstacles include storage technology and initial investment costs."},
             {"speaker": "You", "line": "Nevertheless, the long-term benefits are substantial. Renewable energy reduces carbon emissions and creates new jobs."},
             {"speaker": "Audience", "line": "What do you think about nuclear energy as an alternative?"},
             {"speaker": "You", "line": "That's an excellent question. While nuclear energy is low-carbon, it raises concerns about waste management and safety."},
             {"speaker": "You", "line": "In conclusion, transitioning to renewable energy is not just desirable but essential for our planet's future."},
             {"speaker": "You", "line": "Thank you for your attention. Are there any other questions?"}
         ]), "Academic"),

        ("Business Negotiation", "Practice negotiating in a professional context.", "B2",
         json.dumps([
             {"speaker": "Client", "line": "Thank you for meeting with us. We'd like to discuss the terms of the contract."},
             {"speaker": "You", "line": "Absolutely. We've reviewed your proposal and have some suggestions."},
             {"speaker": "Client", "line": "We're open to discussion. What are your main concerns?"},
             {"speaker": "You", "line": "Primarily, we'd like to renegotiate the delivery timeline. Three months might be too tight for this scope."},
             {"speaker": "Client", "line": "We understand, but we have a product launch scheduled. What would you suggest?"},
             {"speaker": "You", "line": "We could deliver the core features in three months and the remaining features in a second phase."},
             {"speaker": "Client", "line": "That could work. What about the pricing?"},
             {"speaker": "You", "line": "Given the phased approach, we could offer a 10% discount on the total package."},
             {"speaker": "Client", "line": "That sounds reasonable. Let's draft the revised terms."},
             {"speaker": "You", "line": "Excellent. I'll have our team prepare the updated proposal by the end of the week."}
         ]), "Business"),
    ]

    for title, description, level, dialogue, category in speaking_data:
        cursor.execute(
            'INSERT INTO speaking_scenarios (title, description, level, dialogue, category) VALUES (?, ?, ?, ?, ?)',
            (title, description, level, dialogue, category)
        )

    # ═══════════════════════════════════════════
    # BADGES
    # ═══════════════════════════════════════════

    badges_data = [
        ("First Steps", "Complete your first lesson", "🎯", "grammar", 1),
        ("Word Collector", "Learn 10 vocabulary words", "📚", "vocab", 10),
        ("Vocabulary Master", "Learn 50 vocabulary words", "🏆", "vocab", 50),
        ("Word Wizard", "Learn 100 vocabulary words", "✨", "vocab", 100),
        ("Quiz Starter", "Complete 5 quizzes", "📝", "quiz", 5),
        ("Quiz Champion", "Complete 25 quizzes", "🥇", "quiz", 25),
        ("Quiz Legend", "Complete 100 quizzes", "👑", "quiz", 100),
        ("Grammar Beginner", "Complete 3 grammar lessons", "📖", "grammar", 3),
        ("Grammar Master", "Complete 10 grammar lessons", "🎓", "grammar", 10),
        ("3-Day Streak", "Maintain a 3-day streak", "🔥", "streak", 3),
        ("7-Day Streak", "Maintain a 7-day streak", "💪", "streak", 7),
        ("30-Day Streak", "Maintain a 30-day streak", "⭐", "streak", 30),
        ("XP Hunter", "Earn 100 XP", "💎", "xp", 100),
        ("XP Master", "Earn 500 XP", "🌟", "xp", 500),
        ("XP Legend", "Earn 1000 XP", "🏅", "xp", 1000),
    ]

    for name, desc, icon, req_type, req_value in badges_data:
        cursor.execute(
            'INSERT INTO badges (name, description, icon, requirement_type, requirement_value) VALUES (?, ?, ?, ?, ?)',
            (name, desc, icon, req_type, req_value)
        )

    # ═══════════════════════════════════════════
    # WRITING PROMPTS
    # ═══════════════════════════════════════════

    writing_prompts_data = [
        # A1
        ("Describe your family. Who are they? What do they do?", "A1", "Write 3-5 simple sentences about your family members.", "Family"),
        ("Write about your daily routine. What do you do every day?", "A1", "Use present simple tense. Example: I wake up at 7 AM.", "Daily Life"),
        ("Describe your best friend. What do they look like? What do they like?", "A1", "Use simple adjectives: tall, short, funny, kind.", "People"),
        ("Write about your favorite food. Why do you like it?", "A1", "Use words like: delicious, favorite, eat, cook.", "Food"),
        ("Describe your house or apartment. How many rooms are there?", "A1", "Use 'there is' and 'there are' to describe rooms.", "Places"),

        # A2
        ("Write about your last vacation. Where did you go? What did you do?", "A2", "Use past simple tense. Example: I visited...", "Travel"),
        ("Compare two cities you know. How are they different?", "A2", "Use comparatives: bigger, more interesting, cheaper.", "Places"),
        ("Write about a movie you watched recently. Did you like it? Why?", "A2", "Use past tense and opinion expressions.", "Entertainment"),
        ("Describe what you are doing right now and your plans for today.", "A2", "Use present continuous and 'going to' for plans.", "Daily Life"),
        ("Write about a person you admire. Why do you admire them?", "A2", "Use adjectives to describe personality: brave, smart, kind.", "People"),

        # B1
        ("Do you think social media has more positive or negative effects? Explain your opinion.", "B1", "Use linking words: however, furthermore, in my opinion.", "Technology"),
        ("Write about a difficult experience and what you learned from it.", "B1", "Use past tenses and reflection vocabulary.", "Personal"),
        ("Should students wear uniforms at school? Write your opinion.", "B1", "Present arguments for and against.", "Education"),
        ("Describe the environmental problems in your city and suggest solutions.", "B1", "Use vocabulary related to environment and suggestions.", "Environment"),
        ("Write about your career goals and how you plan to achieve them.", "B1", "Use future tenses and conditional sentences.", "Work"),

        # B2
        ("Discuss the advantages and disadvantages of artificial intelligence in education.", "B2", "Use formal language and advanced linking words.", "Technology"),
        ("Write a formal email to a company applying for an internship.", "B2", "Follow formal email conventions.", "Business"),
        ("Is globalization beneficial for developing countries? Discuss both sides.", "B2", "Use academic vocabulary and provide evidence.", "Society"),
        ("Write a review of a book you recently read.", "B2", "Include a summary, analysis, and personal response.", "Literature"),
        ("Discuss the impact of climate change on future generations.", "B2", "Use advanced vocabulary and complex sentence structures.", "Environment"),
    ]

    for prompt, level, hint, category in writing_prompts_data:
        cursor.execute(
            'INSERT INTO writing_prompts (prompt, level, hint, category) VALUES (?, ?, ?, ?)',
            (prompt, level, hint, category)
        )

    conn.commit()
    conn.close()
    print("Database seeded successfully!")


if __name__ == '__main__':
    from models import init_db
    init_db()
    seed_all()
