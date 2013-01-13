/*
 * Copyright © 2009 Scott Perry
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

#ifndef _KEYCODES_H_
#define _KEYCODES_H_ 1
#include <stdint.h>
#include <avr/pgmspace.h>

#define NC          0x00
#define NC16        0xFF00
#define ERR			0xBF /* ¿ */

#define XON         0x1013
#define XOFF        0x1011

// 0x1{1..4} in ASCII refers to special device control codes.  perfect.
#define SHIFT       0x11
//#define SHIFT       0x000
#define CODE        0x12
#define ALT         0x14
// special case for shift lock
#define SHIFT_LOCK  0x13

// from the ISO-8859-1 Character Set
#define CENT       0xa2  /* ¢ */
#define SECTION    0xa7  /* § */
#define DEGREE     0xb0  /* ° */
#define PLUSMINUS  0xb1  /* ± */
#define SQUARE     0xb2  /* ² */
#define CUBE       0xb3  /* ³ */
#define PARAGRAPH  0xb6  /* ¶ */
#define QUARTER    0xbc  /* ¼ */
#define HALF       0xbd  /* ½ */

#define EXPR        0xC0
#define RELOC       0xC1
#define CORRECT     0xC2
#define W_OUT       0xC3
#define BSHALF      0xC4
#define L_OUT       0xC5
#define RESET       0xC6
#define _SWITCH     0xC7
#define REV         0xC8
#define INDEX       0xC9
#define P_INS       0xCA
#define VIEW        0xCB
#define _DEMO       0xCC
#define W_SPELL     0xCD
#define PITCH       0xCE
#define LINE        0xCF
#define M_REL       0xD0
#define L_MAR       0xD1
#define R_MAR       0xD2
#define T_SET       0xD3
#define DT_SET      0xD4
#define T_CLR       0xD5
#define CTR         0xD6
#define RMF         0xD7
#define UNDLN       0xD8
#define BOLD        0xD9
#define OPERATE     0xDA

// table[scannum * 8 + signum + meta * 16]
// across: signum
// vert: scannum
const PROGMEM uint8_t keycodes[] = {
// META: B0000
// 0          1           2           3           4           5           6           7
   ',',       '/',        '1',        '3',        '7',        '5',        '-',        '9',        // 0
   '.',       PLUSMINUS,  '2',        '4',        '8',        '6',        '=',        '0',        // 1
   HALF,      'q',        'e',        't',        'o',        'u',        'n',        'v',        // 2
   ';',       'z',        'f',        'h',        's',        'k',        'x',        'c',        // 3
   ']',       'w',        'r',        'y',        'p',        'i',        'm',        'b',        // 4
   '\'',      'a',        'g',        'j',        'd',        'l',        _SWITCH,    '\t',       // 5
   ' ',       '\n',       W_OUT,      RELOC,      ALT,        '\b',       CORRECT,    CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7
 
//'9','-','5','7','3','1','/',',',
//'0','=','6','8','4','2',PLUSMINUS,'.',
//'v','n','u','o','t','e','q',HALF,
//'c','x','k','s','h','f','z',';',
//'b','m','i','p','y','r','w',']',
//'\t',_SWITCH,'l','d','j','g','a','/',
//CODE,CORRECT,'\b',ALT,RELOC,W_OUT,'\n',' ',
//NC,NC,NC,NC,NC,NC,SHIFT_LOCK,SHIFT,


// across: signum
// vert: scannum
// META: B0001 (SHIFT)
// 0          1           2           3           4           5           6           7
   ',',       '?',        '!',        '#',        '&',        '%',        '_',        '(',        // 0
   '.',       DEGREE,     '@',        '$',        '*',        CENT,       '+',        ')',        // 1
   QUARTER,   'Q',        'E',        'T',        'O',        'U',        'N',        'V',        // 2
   ':',       'Z',        'F',        'H',        'S',        'K',        'X',        'C',        // 3
   '[',       'W',        'R',        'Y',        'P',        'I',        'M',        'B',        // 4
   '"',       'A',        'G',        'J',        'D',        'L',        _SWITCH,    '\t',       // 5
   ' ',       '\n',       W_OUT,      RELOC,      ALT,        '\b',       CORRECT,    CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7

// across: signum
// vert: scannum
// META: B0010 (CODE)
// 0          1           2           3           4           5           6           7
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 0
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 1
   NC,        RESET,      NC,         NC,         REV,        '>',        NC,         CUBE,       // 2
   NC,        SECTION,    NC,         NC,         NC,         NC,         SQUARE,     NC,         // 3
   NC,        '<',        NC,         PARAGRAPH,  INDEX,      NC,         VIEW,       NC,         // 4
   NC,        P_INS,      NC,         NC,         NC,         NC,         _SWITCH,    NC,         // 5
   NC,        EXPR,       L_OUT,      BSHALF,     ALT,        '\b',       NC,         CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7

// across: signum
// vert: scannum
// META: B0011 (CODE + SHIFT)
// 0          1           2           3           4           5           6           7
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 0
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 1
   NC,        RESET,      NC,         NC,         REV,        '>',        NC,         CUBE,       // 2
   NC,        SECTION,    NC,         NC,         NC,         NC,         SQUARE,     NC,         // 3
   NC,        '<',        NC,         PARAGRAPH,  INDEX,      NC,         VIEW,       NC,         // 4
   NC,        P_INS,      NC,         NC,         NC,         NC,         _SWITCH,    NC,         // 5
   NC,        EXPR,       L_OUT,      BSHALF,     ALT,        '\b',       NC,         CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7

// across: signum
// vert: scannum
// META: B0100 (ALT)
// 0          1           2           3           4           5           6           7
   NC,        NC,         PITCH,      M_REL,      DT_SET,     R_MAR,      UNDLN,      CTR,        // 0
   NC,        W_SPELL,    LINE,       L_MAR,      T_CLR,      T_SET,      BOLD,       RMF,        // 1
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 2
   NC,        NC,         NC,         NC,         _DEMO,      NC,         NC,         NC,         // 3
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 4
   NC,        NC,         NC,         NC,         NC,         NC,         _SWITCH,    NC,         // 5
   NC,        NC,         NC,         OPERATE,    ALT,        NC,         NC,         CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7

// across: signum
// vert: scannum
// META: B0101 (ALT + SHIFT)
// 0          1           2           3           4           5           6           7
   NC,        NC,         PITCH,      M_REL,      DT_SET,     R_MAR,      UNDLN,      CTR,        // 0
   NC,        W_SPELL,    LINE,       L_MAR,      T_CLR,      T_SET,      BOLD,       RMF,        // 1
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 2
   NC,        NC,         NC,         NC,         _DEMO,      NC,         NC,         NC,         // 3
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 4
   NC,        NC,         NC,         NC,         NC,         NC,         _SWITCH,    NC,         // 5
   NC,        NC,         NC,         OPERATE,    ALT,        NC,         NC,         CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7

// across: signum
// vert: scannum
// META: B0110 (ALT + CODE)
// 0          1           2           3           4           5           6           7
   NC,        NC,         PITCH,      M_REL,      DT_SET,     R_MAR,      UNDLN,      CTR,        // 0
   NC,        W_SPELL,    LINE,       L_MAR,      T_CLR,      T_SET,      BOLD,       RMF,        // 1
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 2
   NC,        NC,         NC,         NC,         _DEMO,      NC,         NC,         NC,         // 3
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 4
   NC,        NC,         NC,         NC,         NC,         NC,         _SWITCH,    NC,         // 5
   NC,        NC,         NC,         OPERATE,    ALT,        NC,         NC,         CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7

// across: signum
// vert: scannum
// META: B0111 (ALT + CODE + SHIFT)
// 0          1           2           3           4           5           6           7
   NC,        NC,         PITCH,      M_REL,      DT_SET,     R_MAR,      UNDLN,      CTR,        // 0
   NC,        W_SPELL,    LINE,       L_MAR,      T_CLR,      T_SET,      BOLD,       RMF,        // 1
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 2
   NC,        NC,         NC,         NC,         _DEMO,      NC,         NC,         NC,         // 3
   NC,        NC,         NC,         NC,         NC,         NC,         NC,         NC,         // 4
   NC,        NC,         NC,         NC,         NC,         NC,         _SWITCH,    NC,         // 5
   NC,        NC,         NC,         OPERATE,    ALT,        NC,         NC,         CODE,       // 6
   SHIFT,     SHIFT_LOCK, NC,         NC,         NC,         NC,         NC,         NC,         // 7
};

// 0xMETA SIGNAL SCAN
const PROGMEM uint16_t ascii[] = {
  NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16,/* (eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   0x723, /*(bel)*/
  0x066, /*(bs)*/   0x075, /*(ht)*/    0x057, /*(nl)*/   NC16, /*(vt)*/   0x215, /*(np)*/   0x057,/*(cr)*/    NC16, /*(so)*/    NC16, /*(si)*/
  NC16, /*(dle)*/   XON, /*(dc1)*/    NC16, /*(dc2)*/   XOFF, /*(dc3)*/   NC16, /*(dc4)*/   NC16, /*(nak)*/   NC16, /*(syn)*/   NC16, /*(etb)*/
  NC16, /*(can)*/   NC16, /*(em)*/    0x037, /*(sub)*/   NC16, /*(esc)*/   NC16, /*(fs)*/    NC16, /*(gs)*/    NC16, /*(rs)*/    NC16, /*(us)*/
  0x007, /*(sp)*/   0x111, /* ! */    0x120, /* " */    0x131, /* # */    0x130, /* $ */    0x141, /* % */    0x171, /* & */    0x170, /* ' */
  0x161, /* ( */    0x160, /* ) */    0x140, /* * */    0x151, /* + */    0x004, /* , */    0x050, /* - */    0x003, /* . */    0x005, /* / */
  0x060, /* 0 */    0x011, /* 1 */    0x020, /* 2 */    0x031, /* 3 */    0x030, /* 4 */    0x041, /* 5 */    0x040, /* 6 */    0x071, /* 7 */
  0x070, /* 8 */    0x061, /* 9 */    0x103, /* : */    0x001, /* ; */    0x214, /* < */    0x051, /* = */    0x252, /* > */    0x105, /* ? */
  0x121, /* @ */    0x153, /* A */    0x114, /* B */    0x124, /* C */    0x143, /* D */    0x122, /* E */    0x123, /* F */    0x133, /* G */
  0x113, /* H */    0x115, /* I */    0x173, /* J */    0x172, /* K */    0x162, /* L */    0x174, /* M */    0x154, /* N */    0x152, /* O */
  0x155, /* P */    0x142, /* Q */    0x125, /* R */    0x163, /* S */    0x132, /* T */    0x112, /* U */    0x134, /* V */    0x145, /* W */
  0x144, /* X */    0x135, /* Y */    0x164, /* Z */    0x104, /* [ */    NC16,  /* \ */    0x004, /* ] */    NC16, /* ^ */     0x150, /* _ */
  0x010, /* ` */    0x053, /* a */    0x014, /* b */    0x024, /* c */    0x043, /* d */    0x022, /* e */    0x023, /* f */    0x033, /* g */
  0x013, /* h */    0x015, /* i */    0x073, /* j */    0x072, /* k */    0x062, /* l */    0x074, /* m */    0x054, /* n */    0x052, /* o */
  0x055, /* p */    0x042, /* q */    0x025, /* r */    0x063, /* s */    0x032, /* t */    0x012, /* u */    0x034, /* v */    0x045, /* w */
  0x044, /* x */    0x035, /* y */    0x064, /* z */    NC16, /* { */     NC16, /* | */     NC16, /* } */     0x021, /* ~ */     NC16, /*(del)*/
};

//const PROGMEM uint16_t ascii[] = {
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   0x070, /*a*/      0x071, /*b*/  0x072, /*c*/  0x073, /*d*/   0x074, /*e*/   0x075, /*f*/  0x076, /*g*/
  //0x077, /*h*/   0x078, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
  //NC16, /*(nul)*/   NC16, /*(soh)*/   NC16, /*(stx)*/   NC16, /*(etx)*/   NC16, /*(eot)*/   NC16, /*(enq)*/   NC16, /*(ack)*/   NC16, /*(bel)*/
//};
  

// special special characters get special-cased.  heck with 'em.
const PROGMEM uint16_t extended[] = {
  // special characters not anywhere near ASCII, these indices line up with the #defines at the top of the file.
  0x0151, /* ¢ */
  NC16,NC16,NC16,NC16,
  0x0213, /* § */
  NC16,NC16,NC16,NC16,NC16,NC16,NC16,NC16,
  0x0111, /* ° */
  0x0011, /* ± */
  0x0263, /* ² */
  0x0272, /* ³ */
  NC16,NC16,
  0x0234, /* ¶ */
  NC16,NC16,NC16,NC16,NC16,
  0x0102, /* ¼ */
  0x0002, /* ½ */
  //0x000, /* ordf */
  //0x002 /*˜n */
  
  
  /*
  //caracteres especiales, buscar remplazo en ascii para poder controlarlos
  0x017 // alt o backspace
  0x026 // cubierta abierta
  0x037 // replace
  0x046 // move right
  0x056 // move down / paste
  0x065 // caps lock
  0x066 // suggestion
  0x067 // search
  0x076 // left, delete
  
  */
};

const PROGMEM uint16_t control[] = {
  0x216, /* EXPR */
  0x006, /* RELOC */
  0x077, /* CORRECT -- recommend using \b instead */
  0x065, /* _SWITCH */
  0x047, /* W_OUT */
  0x236, /* BSHALF */
  0x226, /* L_OUT */
  0x212, /* RESET */
  0x242, /* REV */
  0x036, /* INDEX */
  0x215, /* P_INS */
  0x264, /* VIEW */
  0x443, /* _DEMO */
  0x411, /* W_SPELL */
  0x420, /* PITCH */
  0x421, /* LINE */
  0x430, /* M_REL */
  0x431, /* L_MAR */
  0x450, /* R_MAR */
  0x451, /* T_SET */
  0x440, /* DT_SET */
  0x441, /* T_CLR */
  0x470, /* CTR */
  0x471, /* RMF */
  0x460, /* UNDLN */
  0x461, /* BOLD */
  0x436, /* OPERATE */
};
#endif // _KEYCODES_H_
