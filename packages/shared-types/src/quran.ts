export interface WordAddress {
  surahNumber: number;
  ayahNumber: number;
  wordPosition: number;
}

export interface WordSelection {
  surahNumber: number;
  ayahNumber: number;
  wordStart: number;
  wordEnd: number;
}

export interface QFWord {
  id: number;
  position: number;
  text_uthmani: string;
  text_imlaei: string;
  transliteration: string;
  translation: string;
  char_type_name: 'word' | 'end' | 'pause' | 'sajdah' | 'rub-el-hizb';
}

export interface QFVerse {
  id: number;
  verse_number: number;
  verse_key: string;
  words: QFWord[];
}

export interface QFAudioSegment {
  word_index: number;
  start_ms: number;
  end_ms: number;
}
