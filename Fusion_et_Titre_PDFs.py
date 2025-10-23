import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import tempfile
import io
import re

def key(x):
    var_nb = re.findall('\d+', x)
    if len(var_nb) ==0:
        var_nb = [0]
    print(var_nb)
    return int(var_nb[0])
        
def Ajout_Titre(input_pdf, watermark_source, Police, color, transparency, scale, pos_y, pos_x):
    reader = PdfReader(io.BytesIO(input_pdf))
    writer = PdfWriter()

    for page in reader.pages:
        # Dimensions de la page
        largeur = float(page.mediabox.width)
        hauteur = float(page.mediabox.height)

        # Créer un calque temporaire avec "Annexe"
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(largeur, hauteur))
        
        # Position du texte selon valeurs normalisées 0–1
        x = pos_x * largeur
        y = pos_y * hauteur
        c.setFillAlpha(transparency)
        c.setFont(Police, scale)
        c.setFillColorRGB(color[0]/255,color[1]/255,color[2]/255)
        c.drawCentredString(x, y, watermark_source)
        c.save()

        # Fusionner la page originale avec le texte
        packet.seek(0)
        watermark = PdfReader(packet)
        page.merge_page(watermark.pages[0])
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def main():
    st.title("📚 Fusion et Titre PDFs")

    uploaded_files = st.file_uploader("", accept_multiple_files=True, type="pdf")
    Classement = ["Par ordre d'importation"] + ["Par ordre alphabétique"] + ["Par ordre numérique"]
    selection0 = st.selectbox("Classement", options=Classement)
    filenames = [f.name for f in uploaded_files]
    
    if selection0 == "Par ordre d'importation" and uploaded_files:
        st.write("Vous pouvez réorganiser les fichiers :")
        # Interface de tri
        order = st.data_editor(
            [{"Ordre": i+1, "Fichier": name} for i, name in enumerate(filenames)],
            num_rows="fixed",
            use_container_width=True,
            key="order_editor"
        )
        ordered_files = [row["Fichier"] for row in sorted(order, key=lambda x: x["Ordre"])]
        
    elif selection0 == "Par ordre alphabétique":
         st.write("Vous pouvez réorganiser les fichiers :")
         filenames=sorted(filenames)
         order = st.data_editor(
            [{"Ordre": i+1, "Fichier": name} for i, name in enumerate(filenames)],
            num_rows="fixed",
            use_container_width=True,
            key="order_editor"
        )
         ordered_files = [row["Fichier"] for row in sorted(order, key=lambda x: x["Ordre"])]

    elif selection0 == "Par ordre numérique":
         st.write("Vous pouvez réorganiser les fichiers :")
         filenames=sorted(filenames, key=key)
         order = st.data_editor(
            [{"Ordre": i+1, "Fichier": name} for i, name in enumerate(filenames)],
            num_rows="fixed",
            use_container_width=True,
            key="order_editor"
        )
         ordered_files = [row["Fichier"] for row in sorted(order, key=lambda x: x["Ordre"])]
    
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
    
    st.info(f"{selection}",icon="📟")

    
    st.markdown("### 📏Position")
    Largeur = st.slider("↔️ Position horizontale du texte (0 = gauche, 1 = droite)", 0.0, 1.0, 0.5, 0.01)
    Hauteur = st.slider("↕️ Position verticale du texte (0 = bas, 1 = haut)", 0.0, 1.0, 0.5, 0.01)
    
    
    st.markdown("### 🌈Personnalisation")
    
    P = ["Helvetica-Bold"] + ["Courier"] + ["Courier-Bold"] + ["Courier-BoldOblique"] + ["Courier-Oblique"] + ["Helvetica"] + ["Helvetica-BoldOblique"] + ["Helvetica-Oblique"] + ["Times-Bold"] + ["Times-BoldItalic"] + ["Times-Italic"] + ["Times-Roman"]
    Police = st.selectbox("Type de police", options=P)
    
    chaine = 'ABCDEFGHIJKLMNOPQRSTUVWYXZ'
    scale = st.slider("Taille police", 0, 50, 30)
    hexa = st.color_picker("Couleur", "#2F99F3")
    color = hex_to_rgb(hexa)
    transparency = st.slider("Transparence", 0.0, 1.0, 0.3)
    Name_end = st.text_input('Nom du PDF en sortie :', value="Fusion_et_Titre_PDFs") 
    i = 0
    if st.button("⚡ Lancer"):
        if uploaded_files :
            UFs=[]
            for name in ordered_files:
                file = next(f for f in uploaded_files if f.name == name)
                UFs.append(file)  
            merged_pdf = PdfWriter()
            for uploaded_file in UFs:
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
                
                watermarked_pdf = Ajout_Titre(uploaded_file.read(), name, Police, color, transparency, scale, Hauteur, Largeur)
                reader = PdfReader(watermarked_pdf)
                for page in reader.pages:
                    merged_pdf.add_page(page)
                i=i+1
            temp_merged_pdf = tempfile.NamedTemporaryFile(delete=False)
            merged_pdf.write(temp_merged_pdf)
            temp_merged_pdf.close()
            
        with open(temp_merged_pdf.name, "rb") as f:    
            st.download_button(
                label="✔️ Télécharger",
                data=f,
                file_name=Name_end + ".pdf",
                mime="application/pdf"
            )
            
if __name__ == "__main__":

    main()
























