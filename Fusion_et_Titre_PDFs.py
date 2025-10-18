import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import tempfile
import io
import re

def key(x):
    var_nb = re.findall('\d+', x.name)
    if len(var_nb) ==0:
        var_nb = [0]
    print(var_nb)
    return int(var_nb[0])
        
def add_watermark(input_pdf, watermark_source, Police, color, transparency, scale, Hauteur, Largeur):
    
    watermark_pdf = io.BytesIO()
    c = canvas.Canvas(watermark_pdf, pagesize=A4)
    c.setFillAlpha(transparency)
    c.setFont(Police, scale)
    c.setFillColorRGB(color[0]/255,color[1]/255,color[2]/255)
    c.drawString(Largeur * cm, (29.7-Hauteur) * cm, watermark_source)

    c.save()
    watermark_pdf.seek(0)
    

    input_pdf = PdfReader(input_pdf)
    watermark_pdf = PdfReader(watermark_pdf)
    output_pdf = PdfWriter()
    
    for i in range(len(input_pdf.pages)):
        page = input_pdf.pages[i]
        page.merge_page(watermark_pdf.pages[0])
        output_pdf.add_page(page)
    
    output_pdf_stream = io.BytesIO()
    output_pdf.write(output_pdf_stream)
    output_pdf_stream.seek(0)
    
    return output_pdf_stream

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def main():
    st.title("📚 Fusion et Titre PDFs")

    uploaded_files = st.file_uploader("", accept_multiple_files=True, type="pdf")
    Classement = ["Par ordre d'importation"] + ["Par ordre alphabétique"] + ["Par ordre numérique"]
    selection0 = st.selectbox("Classement", options=Classement)
    
    if selection0 == "Par ordre d'importation":
        Info_ordre = "1ère import = 1er doc, 2ème import = 2ème doc, ..."
    elif selection0 == "Par ordre alphabétique":
        st.markdown('''ℹ En fonction du titre du PDF : 
        1)A15.pdf 
        2)G2.pdf 
        3)M9.pdf''')
    elif selection0 == "Par ordre numérique":
        st.markdown'''En fonction du nombre présent dans le titre du PDF : 
        1)G2.pdf 
        2)M9.pdf 
        3)A15.pdf''')

    
    st.markdown("### ✍🏻Format")
    
    Titre1 = ["Annexe"] + ["Autre Titre"] + ["Sans"]
    selection1 = st.selectbox("Selection du Titre_1", options=Titre1)
    
    if selection1 == "Autre Titre": 
        otherOption1 = st.text_input("Entrer votre Titre")
        
    Incr = ["A,B,C,.."] + ["1,2,3,.."] + ["Sans"]
    selection2 = st.selectbox("Incrément :", options=Incr)
    
    Titre2 = ["Sans"] + ["Titre existant du PDF"]
    selection3 = st.selectbox("Selection du Titre_2", options=Titre2)
    
    if selection1 == "Autre Titre":
        Titre_1 = otherOption1
    elif selection1 == "Sans":
        Titre_1 = ''
    else :
        Titre_1 = selection1
    
    if selection3 == "Sans":
        Titre_2 = ''
    else :
        Titre_2 = selection3
        if selection1 == "Sans" and selection2 !="Sans":
            Titre_2 = '. ' + Titre_2
        elif selection1 != "Sans" and selection2 =="Sans" :
            Titre_2 = ' : ' + Titre_2
        elif selection1 != "Sans" and selection2 !="Sans" :
            Titre_2 = ' : ' + Titre_2
    
    if selection2 == "A,B,C,..":
        Increment = ' A'
    elif selection2 == "1,2,3,..":
        Increment = ' 1'
    elif selection2 == "Sans": 
        Increment = ''
    
    selection = Titre_1 + Increment + Titre_2
    
    st.info(selection,icon="📟")

    
    st.markdown("### 📏Position")
    Hauteur = st.slider("↕️ Hauteur (Partant du haut) 0 à 29,7cm", 0.0, 29.7, 0.7)
    Largeur = st.slider("↔️ Largeur (Partant de la gauche) 0 à 21cm", 0.0, 21.0, 1.0)
    
    st.markdown("### 🌈Personnalisation")
    
    P = ["Helvetica-Bold"] + ["Courier"] + ["Courier-Bold"] + ["Courier-BoldOblique"] + ["Courier-Oblique"] + ["Helvetica"] + ["Helvetica-BoldOblique"] + ["Helvetica-Oblique"] + ["Times-Bold"] + ["Times-BoldItalic"] + ["Times-Italic"] + ["Times-Roman"]
    Police = st.selectbox("Type de police", options=P)
    
    chaine = 'ABCDEFGHIJKLMNOPQRSTUVWYXZ'
    scale = st.slider("Taille police", 0, 50, 14)
    hexa = st.color_picker("Couleur", "#000000")
    color = hex_to_rgb(hexa)
    transparency = st.slider("Transparence", 0.0, 1.0, 1.0)
    
    i = 0
    if st.button("⚡ Lancer"):

        if uploaded_files :
            if selection0 == "Par ordre alphabétique":
                UFs = sorted(uploaded_files, key=lambda uploaded_files: uploaded_files.name)
                print(UFs[0].name, 'A')
            elif selection0 == "Par ordre numérique":
                UFs = sorted(uploaded_files, key=key)
                print(UFs[0].name, 'N')
            else:
                UFs = uploaded_files
                print(UFs[0].name, 'O')  
            merged_pdf = PdfWriter()
            for uploaded_file in UFs:
                print(uploaded_file.name[:-4])
                
                if selection2 == "A,B,C,..":
                    Increm = str(' '+chaine[i])
                elif selection2 == "1,2,3,..":
                    nb = str(i+1)
                    Increm = str(' '+nb)
                else:
                    Increm = ''
                
                if selection3 == "Titre existant du PDF":
                    Titre_2 = uploaded_file.name[:-4]
                    if selection1 == "Sans" and selection2 !="Sans":
                        Titre_2 = '. ' + Titre_2
                    elif selection1 != "Sans" and selection2 =="Sans" :
                        Titre_2 = ' : ' + Titre_2
                    elif selection1 != "Sans" and selection2 !="Sans" :
                        Titre_2 = ' : ' + Titre_2
                         
                name = Titre_1 + Increm + Titre_2 
                
                watermarked_pdf = add_watermark(uploaded_file, name, Police, color, transparency, scale, Hauteur, Largeur)
                reader = PdfReader(watermarked_pdf)
                for page in reader.pages:
                    merged_pdf.add_page(page)
                i=i+1
            temp_merged_pdf = tempfile.NamedTemporaryFile(delete=False)
            merged_pdf.write(temp_merged_pdf)
            temp_merged_pdf.close()
            watermarked_pdf_stream = add_watermark(temp_merged_pdf.name, '', Police, color, 0.0, scale, Hauteur, Largeur)
            
            
            st.download_button(
                label="✔️ Télécharger",
                data=watermarked_pdf_stream,
                file_name="Annexe.pdf",
                mime="application/pdf"
            )
            
if __name__ == "__main__":

    main()













