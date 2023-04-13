def process_text(text, emoji_dict, teen_dict, wrong_lst,english_lst):
    from underthesea import word_tokenize, pos_tag, sent_tokenize
    import regex
    document = text.lower()
    document = document.replace("’",'')
    document = regex.sub(r'\.+', ".", document)
    new_sentence =''
    for sentence in sent_tokenize(document):
        # if not(sentence.isascii()):
        ###### CONVERT EMOJICON
        sentence = ''.join(emoji_dict[word]+' ' if word in emoji_dict else word for word in list(sentence))
        sentence = ''.join(english_lst[word]+' ' if word in english_lst else word for word in list(sentence))
        ###### CONVERT TEENCODE
        sentence = ' '.join(teen_dict[word] if word in teen_dict else word for word in sentence.split())
        ###### DEL Punctuation & Numbers
        pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
        sentence = ' '.join(regex.findall(pattern,sentence))
        ###### DEL wrong words   
        sentence = ' '.join('' if word in wrong_lst else word for word in sentence.split())
        ###### DEL  words 
        sentence = ' '.join('' if len(word)>7  else word for word in sentence.split())
        new_sentence = new_sentence+ sentence + '. '                    
    document = new_sentence   
    #print(document)
    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    #...
    return document 
def process_emoji(text):
    from underthesea import word_tokenize, pos_tag, sent_tokenize
    import regex
    kk=['—', 'l', '…', '•', ';', '–', 'k', 'c', '“', '”', 'a', '▲',
       '\uf043', 'ủ', 'b', 'm', 'd', 'đ', '_', '|', 'v', '➦', '?', '✧',
       '►', 'e', 'ô', '★', '̣', '𝐚', '̉', '̀', '̛', '𝐢', '̃', '𝐨', '̂',
       '𝐧', 'j', 'y', 't', 'o', '→', '✚', 'h', 'u', '♡', 'x', '✦', '✪',
       'w', '☞', '❆', '【', '】', '𝗔', '́', 'r', '●', '¬', 'p', 'q', '$',
       '@', '¦', 'n', '·', '■', 's', 'z', '❥', '̆', '𝗰', '𝗽', '𝗻', '𝗶',
       '𝗮', '𝗢', '𝗦', '𝗠', '𝗟', '、', "'", '𝑨', '𝒐', '！', '\uf0a7', '☆',
       '°', '\\', '\u202a', '○', 'f', '₫', '◤', '◆', '┈', '͟', 'g', 'ẫ',
       'ặ', '\u200d', 'ứ', '�', '\uf0d6', '\uf0fc', '\uf0d8', '：', '𝑜',
       '𝑛', '𝑖', '𝑎', 'é', '𝗼', 'ố', '※', '±', '╔', '═', '╗', '╚', '╝',
       '𝐋', '𝐍', '{', '}', '✩', 'ò', '✐', '，', '②', '③', '④', '⑤', '❖',
       '\x08', '´', 'í', '¥', '➤', '⦁', '♤', '☛', '❀', '（', '）', '𝐌', '‘',
       '’', '▼', '\u202c', '𝗺', '𝘂', '𝘁', '𝗖', '𝗜', '𝒖', '𝒑', '𝒚', '𝒏',
       '𝒊', '𝒕', '✿', '✓', 'ỉ', '￼', '𝙩', '𝐭', '𝐲', '𝙤', '𝙣', '⃣', '▽',
       '穿', '𝓷', '𝓶', '𝐮', '𝐎', '𝐓', '𝐩', '𝐦', '𝐜', '℅', '◔', '𝖙', '𝖚',
       '҉', '☏', '；', '￥', '√', '◉', '～', 'ổ', '𝘆', '𝗧', '𝗸', '⑶', '⑷',
       '𝙞', '𝙪', '𝙢', '𝐈', '`', 'è', 'ự', '◙', '☼', '➣', '𝙏', '𝑶', '🇯',
       '🇪', '🇦', '🇳', '𝖔', '𝖈', '𝖎', '𝖓', '≤', '◑', '\uf0b7', '»', 'â',
       'ⓛ', 'ⓘ', 'ⓞ', 'ⓝ', 'ⓜ', 'ⓔ', 'ⓢ', 'ⓗ', 'ⓟ', '➫', '✸', '\u2063',
       '𝐘', '𝓸', '𝓽', '̶', 'ẽ', 'ề', 'ầ', 'ọ', 'ĩ', 'ể', 'ị', 'ộ', 'ắ',
       '͡', 'ಥ', '͜', 'ʖ', 'ê', '𝙘', '➊', '➋', '➌', '➍', '➎', '➬',
       '\uf0e8', '֎', '𝗞', '𝑐', '𝑡', '𝑢', '𝑚', '𝗨', '✲', '➜', '✬', 'ì',
       'ậ', 'ẹ', 'ấ', '➥', '𝒂', '✯', 'ả', '𝒄', '𝒎', '。', '\uf076', '×',
       'ẻ', '\x7f', '÷', '∆', '𝓬', '①', '◁', '𝐂', '✮', '◯', '¸', '¯', '◕',
       '‿', '❁', '❦', '▷', 'ø', '𝑻', '𝑴', '𝑵', '½', '∗', '\uf0f0', '⇝',
       '🇰', '🇧', '🇴', '🇾', '❈', '\uf04f', '꧁', '༺', '༒', '༻', '꧂', '┊',
       '\u200c', '－', '𝙰', '𝚘', '𝚒', '𝚢', '𝚗', '𝚊', '𝚌', '𝚙', '𝚝', '𝚖',
       '𝚞', '❉', '⠀', '・', '≧', 'ö', 'ñ', '◐', '̄', 'а', '′', '⌄', '✼',
       'φ', '▹', '∩', 'づ', '╭', '◈', '♛', '\uf06e', '⁃', 'ᴀ', '―', '⇨',
       '⇦', '𝐄', 'ỏ', 'ミ', '彡', '➻', '━', '⇒', 'ợ', '𝙖', '𝒔', '❅', '✫',
       '✭', '✰', '✹', '✷', '✶', '✵', '✱', '❊', '✾', '✽', '✠', '✺', '❋',
       'ụ', '☟', '\uf055', '\uf0ab', '𝐊', '\uf04a', '✻', 'ệ', '₩', '｡',
       '𝐝', '𝐬', '𝑠', '∞', 'ú', 'ẩ', '𝕔', '𝕦', 'ﾉ', 'ﾟ', '∀', 'ω', '◌',
       '⑅', '⃝', '⋆', 'ღ', '◢', 'ế', '𝐀', 'ᴗ', 'ヾ', '╹', '◡', 'ノ', '《',
       '》', '☜', 'の', 'ó', '⛦', 'ã', 'ỗ', '˘', '³', 'ε', '｀', '＾', '℃',
       '士', '﹋', '﹊', '♪', '┅', '苓', '＜', '☊', '◦', '¡', '𝐤', '♘', '襦',
       '≦', '◍', '˃', '🇫', 'ă', '𝙮', '❾', '❷', '꙰', '‡', '˚', '\uf0e0',
       '➢', '\u202d', '⚘', '㎏', 'ᴜ', '➪', '「', '」', '𝘵', '𝘢', '𝘪', '𝘶',
       '𝘮', '𝘯', '☬', '█', 'ி', '🡆', '۞', 'ஐ', 'ũ', '𝒆', '𝑝', '𝑇', 'º',
       '♔', 'δ', '女', '𝙥', '℉', '❶', '❸', '❹', '❺', '𝒉', '𝒅', '𝒈', '𝒌',
       '𝒓', '𝑲', '𝘤', 'ȶ', '✆', '𝐱', '𝐁', '𝗵', '𝘨', '𝘴', 'ỹ', '̧',
       '\uf06c', '\uf045', '\uf0ef', '\uf0c6', '\uf050', '\uf02a', '◎',
       '↓', '▁', '≥', '₱', '◄', '口', '％', '𝐔', '€', '⍣', '𝑦', '𝑒', '⁄',
       '➺', '✘', '𝑪', 'ü', '🅻', '‐', '𝐡', '\uf69a', '\uf4aa', '\ufeff',
       'ᴄ', '♫', '♬', 'ẵ', '⎕', '▸', '∇', 'ﾞ', '𝐴', '≈', '〗', '〖', '□',
       '⁂', '𝕤', '◇', 'ℱ', '𝓢', '⒈', '⒉', '⒊', '⒋', '\uf0f2', '¿', '«',
       '⇛', '‒', '🅺', '➲', '☇', '\uf046', '\uf0bf', '♕', '﹍']
    document = text.lower()
    document = document.replace("’",'')
    document = regex.sub(r'\.+', ".", document)
    new_sentence =''
    for sentence in sent_tokenize(document):

        ###### DEL wrong words   
        sentence = ' '.join('' if word in kk else word for word in sentence.split())
        new_sentence = new_sentence+ sentence + ' '                    
    document = new_sentence   
    #print(document)
    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    return document
def clean_text(text):
    import re
    import emoji
    text_clean=str(text).lower()
    if "thông tin sản phẩm\n" in text_clean:
        text_clean=text_clean[text_clean.index("thông tin sản phẩm\n"):]
    elif "mô tả sản phẩm\n" in text_clean:
        text_clean=text_clean[text_clean.index("mô tả sản phẩm\n"):]
    elif "\n\n" in text_clean:
        text_clean=text_clean[text_clean.index("\n\n"):]
    elif "\ngửi từ\n" in text_clean:
        text_clean=text_clean[text_clean.index("\ngửi từ\n")+len("\ngửi từ\n"):]
    
    # loại bỏ phần size
    text_clean=re.sub(r"\nsize[^\n]*","",text_clean)
    # loại bỏ các hastag
    text_clean=re.sub(r"#[^#]*","",text_clean)
    # loại bỏ các kí tự không hợp lệ
    text_clean=re.sub(r"\n"," ",text_clean)
    text_clean=emoji.replace_emoji(text_clean)
    text_clean=re.sub('[\.\:\,\-\—\+\d\!\...\"\*\>\<\^\&\/\[\]\(\)\=\~\%]',' ',text_clean)
    # loại bỏ các từ không cần thiết
    text_clean=re.sub('\ss\s|\sm\s|\sl\s|\sxl|xxl|xxxl|xxxxl|2xl|3xl|4xl|size|\smm\s|\scm\s|\sm\s|\sg\s|\skg\s',' ',text_clean)
    text_clean=re.sub('\s+',' ',text_clean) 
    # ...
    return text_clean
# Chuẩn hóa unicode tiếng việt
def loaddicchar():
    uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
    unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic
 
# Đưa toàn bộ dữ liệu qua hàm này để chuẩn hóa lại
def covert_unicode(txt):
    import regex
    dicchar = loaddicchar()
    return regex.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)
def process_special_word(text):
    new_text = ''
    text_lst = text.split()
    i= 0
    if 'không' in text_lst:
        while i <= len(text_lst) - 1:
            word = text_lst[i]
            #print(word)
            #print(i)
            if  word == 'không':
                next_idx = i+1
                if next_idx <= len(text_lst) -1:
                    word = word +'_'+ text_lst[next_idx]
                i= next_idx + 1
            else:
                i = i+1
            new_text = new_text + word + ' '
    else:
        new_text = text
    return new_text.strip()
def process_postag_thesea(text):
    from underthesea import word_tokenize, pos_tag, sent_tokenize
    import regex
    new_document = ''
    for sentence in sent_tokenize(text):
        sentence = sentence.replace('.','')
        ###### POS tag
        #lst_word_type = ['N','Np','A','AB','V','VB','VY','R']
        #lst_word_type = ['A','AB','V','VB','VY','R','C']
        #lst_word_type = ['A','AB','V','VB','VY','R','M','C']
        sentence = ' '.join( word[0] for word in pos_tag(word_tokenize(sentence, format="text")))
        new_document = new_document + sentence + ' '
    ###### DEL excess blank space
    new_document = regex.sub(r'\s+', ' ', new_document).strip()
    return new_document
def remove_stopword(text, stopwords):
    import regex
    ###### REMOVE stop words
    document = ' '.join('' if word in stopwords else word for word in text.split())
    #print(document)
    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    return document