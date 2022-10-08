import streamlit as st
import cv2
import time

def main_gui():
    image = r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\background.jpg'
    st.header('Chest X-ray checking using AI')
    st.markdown("***")
    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image)
    st.markdown("***")
    st.write('Đây là website thử nghiệm ứng dụng của AI trong việc kiểm tra bệnh ở phổi.')
    st.write('Để bắt đầu kiểm tra, vui lòng điền thông tin của bạn vào form bên cạnh !!!')
    st.markdown("###")
    st.warning('Website vẫn đang trong quá trình xây dựng và thử nghiệm, kết quả chỉ mang tính chất tham khảo !!!')
    return()

def start():
    with st.sidebar.form('form_1'):
        st.header('Mời bạn nhập thông tin', )
        name = st.text_input("Họ và tên: ")
        age = st.text_input("Độ tuổi: ")
        location = st.text_input("Địa chỉ: ")
        task = st.selectbox("Loại chẩn đoán",["Chẩn đoán Covid19","Phát hiện viêm phổi"])
        st.markdown("***")
        image = st.file_uploader('Ảnh X-ray cần dự đoán:')
        submit = st.form_submit_button("Xác nhận")
    if submit:
        if image and name and location and age:
            if task == "Chẩn đoán Covid19":
                st.sidebar.warning('Thông tin của bạn đã được lưu !')
                time.sleep(0.5)
                st.subheader('Xin chào ' + str(name) + ' !')
                st.markdown("***")
                time.sleep(0.5)
                st.write('Đây là trang web chẩn đoán Covid-19 dựa trên ảnh X-ray của bạn')
                time.sleep(0.5)
                st.write('Kết quả đang được trả về...')
                st.write(' => Chạy mô hình 1...')
                time.sleep(1)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(image, width=448)
                with col2:
                    st.subheader('Kết quả: DƯƠNG TÍNH')
                    st.write('Độ tin cậy: 96%')
                    st.warning(
                        'Website vẫn đang trong quá trình xây dựng và thử nghiệm, kết quả chỉ mang tính chất tham khảo !!!')
            if task == "Phát hiện viêm phổi":
                st.sidebar.warning('Thông tin của bạn đã được lưu !')
                time.sleep(1)
                st.subheader('Xin chào ' + str(name) + ' !')
                st.markdown("***")
                time.sleep(1)
                st.write('Đây là mô hình phát hiện viêm phổi dựa trên ảnh X-ray của bạn')
                time.sleep(1)
                st.write('Kết quả đang được trả về...')
                st.write(' => Chạy mô hình 2...')
                # = cv2.imread(image)
                #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                time.sleep(1)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(image,width=448)
                with col2:
                    st.write('Kết quả chẩn đoán:  LAO PHỔI')
                    st.write('Mức độ tin cậy:  69%')
                    st.warning('Website vẫn đang trong quá trình xây dựng và thử nghiệm, kết quả chỉ mang tính chất tham khảo !!!')
        else:
            st.sidebar.warning('Vui lòng cung cấp đầy đủ thông tin !!!')
            main_gui()

    else:
        main_gui()


start()









#st.title("Chẩn đoán phổi sử dụng ảnh X-Ray")
#st.image(image, caption='Hình ảnh chẩn đoán')
#st.write('Kết quả: Dương tính')