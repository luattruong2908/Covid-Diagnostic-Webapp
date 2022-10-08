import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import cv2
import time
from pyngrok import ngrok
from db_task import *
from predict import *
import pyngrok
from pydicom.data import get_testdata_file

#print(publ_url)
channel = 3
my_test_transforms = transforms.Compose(
    [  # Compose makes it possible to have many transforms
        transforms.ToPILImage(),
        transforms.Grayscale(num_output_channels=channel),
        transforms.Resize((300, 300)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ]
)
def main_gui():
    image = r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\group_of_experts_in_white_PPE.jpg'
    st.header('🤖 BK - VISION 💓')
    #st.markdown("***")
    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image)
    st.markdown("***")
    st.subheader('Tổng quan:')
    st.write('Đây là website thử nghiệm ứng dụng của AI trong việc "Chẩn đoán bệnh ở phổi", '
             'là đề tài LVTN được thực hiện bởi sinh viên trường Đại học Bách Khoa - ĐHQG '
             'TP.HCM cùng giảng viên hướng dẫn.')
    st.write('Để bắt đầu sử dụng công cụ chẩn đoán, bạn phải "Đăng nhập" vào hệ thống bằng'
             ' thanh Menu bên cạnh và nếu chưa có tài khoản bạn có thể chọn "Đăng kí" để '
             'tạo tài khoản mới !')
    st.write('Để bắt đầu sử dụng chức năng chẩn đoán, bạn phải "Đăng nhập" vào hệ thống bằng'
             ' thanh Menu bên cạnh và nếu chưa có tài khoản bạn có thể chọn "Đăng kí" để '
             'tạo tài khoản mới !')
    st.markdown("***")
    st.write('Ứng dụng sử dụng mô hình  EfficientNet-B0 làm công cụ chẩn đoán bệnh !')
    if st.button('Xem thêm về mô hình'):
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            df = pd.read_csv(r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\model_eval.csv')
            df = pd.DataFrame(df)
            st.write(df)
            image1 = r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\cfs_matrix.png'
            image1 = cv2.imread(image1)
            image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
            st.image(image1)
        st.write('Các thông số trên được đánh giá trên một tập kiểm thử có 400 ảnh, 200 ảnh dương tính và 200 ảnh âm tính')
    st.markdown("***")
    st.warning('Website vẫn đang trong quá trình xây dựng và thử nghiệm, kết quả chỉ mang tính chất tham khảo !')
    return ()

def user_gui():
    st.info('Xin chào, ' + str(select(st.session_state['username'],2)) + ' !')
    st.markdown("***")
    with st.sidebar:
        image = cv2.imread(r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\logo.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image)
        st.markdown("***")
        st.success("🧑‍⚕️ Đăng nhập người dùng: " +  str(st.session_state['username']))
        st.markdown("***")
        if st.button("Đăng xuất"):
            st.session_state['login'] = 'notlogin'
            st.experimental_rerun()

    time.sleep(0.5)
    task = st.selectbox("Loaị chẩn đoán:",
                        ["Chẩn đoán Covid-19", "Mô hình khác"])

    if task == "Chẩn đoán Covid-19":
        if st.checkbox('Sử dụng thông tin cá nhân từ tài khoản'):
            with st.form('form'):
                    image = st.file_uploader('Tải ảnh X-quang phổi cần dự đoán vào đây:',type=['png','jpeg','jpg','dcm'])
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        if image:
                            with st.spinner("Đang xử lí..."):
                                st.markdown("***")
                                time.sleep(1)
                                try:
                                    check = Image.open(image)
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.image(image, width=448)
                                    with col3:
                                        st.write('Kết quả chẩn đoán:')
                                        result = prediction(image, my_test_transforms)
                                        res = int(result[0])
                                        confidence = int(result[1])
                                        if res == 1:
                                            st.error('Dương tính')
                                            st.write('Độ tin cậy:')
                                            st.info(str(confidence) + ' %')
                                        else:
                                            st.success('Âm tính')
                                            st.write('Độ tin cậy:')
                                            st.info(str(confidence) + ' %')
                                        image = Image.open(image)
                                        img_name = 'img_' + str(count_file()) + '.png'
                                        image_name = 'C:/Users/TRUONGLUAT/PycharmProjects/LVTN/Image/' + str(img_name)
                                        image.save(image_name)
                                        today = date.today()
                                        today = today.strftime("%Y-%m-%d")
                                        user_name = str(st.session_state['username'])
                                        name = select(str(st.session_state['username']), 2)
                                        age = select(str(st.session_state['username']), 3)
                                        address = select(str(st.session_state['username']), 6)
                                        sex = select(str(st.session_state['username']), 7)
                                        create_resultstable()
                                        add_results(user_name, res, name, age, address, sex, img_name, today)
                                        st.stop()
                                except IOError:
                                    img_name = read_dicom(image)
                                    image_name = 'C:/Users/TRUONGLUAT/PycharmProjects/LVTN/Image/' + str(img_name)
                                    prediction(image_name, my_test_transforms)
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        image = cv2.imread(image_name)
                                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                                        st.image(image, width=448)
                                    with col3:
                                        image = 'C:/Users/TRUONGLUAT/PycharmProjects/LVTN/Image/' + str(img_name)
                                        st.write('Kết quả chẩn đoán:')
                                        result = prediction(str(image), my_test_transforms)
                                        res = int(result[0])
                                        confidence = int(result[1])
                                        if res == 1:
                                            st.error('Dương tính')
                                            st.write('Độ tin cậy:')
                                            st.info(str(confidence) + ' %')
                                        else:
                                            st.success('Âm tính')
                                            st.write('Độ tin cậy:')
                                            st.info(str(confidence) + ' %')
                                        today = date.today()
                                        today = today.strftime("%Y-%m-%d")
                                        user_name = str(st.session_state['username'])
                                        name = select(str(st.session_state['username']), 2)
                                        age = select(str(st.session_state['username']), 3)
                                        address = select(str(st.session_state['username']), 6)
                                        sex = select(str(st.session_state['username']), 7)
                                        create_resultstable()
                                        add_results(user_name, res, name, age, address, sex, img_name, today)
                                        st.stop()

                        else:
                            st.error('Vui lòng chọn ảnh cần chẩn đoán !!!')

        else:
            with st.form('form'):
                name = st.text_input("Họ và tên: ")
                sex = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])
                address = st.selectbox("Địa chỉ:", (
                "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Bến Tre", "Bình Định",
                "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cần Thơ", "Cao bằng", "Đà Nẵng", "Đắk Lắk",
                "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh",
                "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum",
                "Lai Châu",
                "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận",
                "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng",
                "Sơn La", "Tây Ninh",
                "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP. Hồ Chí Minh", "Trà Vinh",
                "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"))
                age = st.date_input("Ngày sinh: ")
                image = st.file_uploader('Tải ảnh X-quang phổi cần dự đoán vào đây:',type=['png','jpeg','jpg','dcm'])
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    if image and name and age and address and sex:
                        st.markdown("***")
                        with st.spinner("Đang xử lí..."):
                            time.sleep(1)
                            try:
                                check = Image.open(image)
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.image(image, width=448)
                                with col3:
                                    st.write('Kết quả chẩn đoán:')
                                    result = prediction(image, my_test_transforms)
                                    res = int(result[0])
                                    confidence = int(result[1])
                                    if res == 1:
                                        st.error('Dương tính')
                                        st.write('Độ tin cậy:')
                                        st.info(str(confidence) + ' %')
                                    else:
                                        st.success('Âm tính')
                                        st.write('Độ tin cậy:')
                                        st.info(str(confidence) + ' %')
                                image = Image.open(image)
                                image_name = r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Image\img_' + str(count_file()) + '.png'
                                img_name = 'img_' + str(count_file()) + '.png'
                                image.save(image_name)
                                today = date.today()
                                today = today.strftime("%Y-%m-%d")
                                print(today)
                                user_name = str(st.session_state['username'])
                                create_resultstable()
                                add_results(user_name, res, name, age, address, sex, img_name, today)
                                st.stop()

                            except IOError:
                                img_name = read_dicom(image)
                                image_name = 'C:/Users/TRUONGLUAT/PycharmProjects/LVTN/Image/' + str(img_name)
                                prediction(image_name, my_test_transforms)
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    image = cv2.imread(image_name)
                                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                                    st.image(image, width=448)
                                with col3:
                                    image = 'C:/Users/TRUONGLUAT/PycharmProjects/LVTN/Image/' + str(img_name)
                                    st.write('Kết quả chẩn đoán:')
                                    result = prediction(str(image), my_test_transforms)
                                    res = int(result[0])
                                    confidence = int(result[1])
                                    if res == 1:
                                        st.error('Dương tính')
                                        st.write('Độ tin cậy:')
                                        st.info(str(confidence) + ' %')
                                    else:
                                        st.success('Âm tính')
                                        st.write('Độ tin cậy:')
                                        st.info(str(confidence) + ' %')
                                    today = date.today()
                                    today = today.strftime("%Y-%m-%d")
                                    user_name = str(st.session_state['username'])
                                    name = select(str(st.session_state['username']), 2)
                                    age = select(str(st.session_state['username']), 3)
                                    address = select(str(st.session_state['username']), 6)
                                    sex = select(str(st.session_state['username']), 7)
                                    create_resultstable()
                                    add_results(user_name, res, name, age, address, sex, img_name, today)
                                    st.stop()

                    else:
                        st.error('Vui lòng điền đầy đủ thông tin !!!')
    else:
        with st.form('form'):
            st.warning('Chức năng vẫn đang trong quá trình hoàn thiện ... ! ⚒️')
            submit = st.form_submit_button("Xác nhận")
        return ()

def admin_gui():
    with st.sidebar:
        image = cv2.imread(r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\logo.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image)
        st.markdown("***")
        st.success("🧑‍💻 Đăng nhập dưới quyền quản trị viên")
        st.markdown("***")
        if st.button("Đăng xuất"):
            st.session_state['login'] = 'notlogin'
            st.experimental_rerun()
    st.header("DASHBOARD 📊")
    task = st.selectbox("HOẠT ĐỘNG:",
                        ["Thông tin người dùng","Thống kê chẩn đoán"])
    if task == "Thông tin người dùng":
        userinfo = pd.DataFrame(displayall(),columns=['Tài khoản','Mật khẩu','Họ và tên','Ngày sinh','Số điện thoại','Email','Vị trí','Giới tính'])
        st.dataframe(userinfo)
        st.markdown("***")
        filter = st.selectbox("LỌC DỮ LIỆU:", ["Lọc theo tài khoản", "Lọc theo tên", "Lọc theo ngày sinh",  "Lọc theo số điện thoại", "Lọc theo mail", "Lọc theo giới tính", "Lọc theo vị trí"])
        with st.form('form_filter'):
            if filter == 'Lọc theo tài khoản':
                info = st.text_input('')
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    filter_info = pd.DataFrame(filter_username(info),
                                            columns=['Tài khoản', 'Mật khẩu', 'Họ và tên', 'Ngày sinh', 'Số điện thoại',
                                                     'Email', 'Vị trí', 'Giới tính'])
                    st.write(filter_info)
            elif filter == 'Lọc theo tên':
                info = st.text_input('')
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    filter_info = pd.DataFrame(filter_name(info),
                                            columns=['Tài khoản', 'Mật khẩu', 'Họ và tên', 'Ngày sinh', 'Số điện thoại',
                                                     'Email', 'Vị trí', 'Giới tính'])
                    st.write(filter_info)
            elif filter == 'Lọc theo ngày sinh':
                info = str(st.date_input("Ngày sinh: "))
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    filter_info = pd.DataFrame(filter_age(info),
                                            columns=['Tài khoản', 'Mật khẩu', 'Họ và tên', 'Ngày sinh', 'Số điện thoại',
                                                     'Email', 'Vị trí', 'Giới tính'])
                    st.write(filter_info)
            elif filter == 'Lọc theo số điện thoại':
                info = st.text_input('')
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    filter_info = pd.DataFrame(filter_phone(info),
                                            columns=['Tài khoản', 'Mật khẩu', 'Họ và tên', 'Ngày sinh', 'Số điện thoại',
                                                     'Email', 'Vị trí', 'Giới tính'])
                    st.write(filter_info)
            elif filter == 'Lọc theo mail':
                info = st.text_input('')
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    filter_info = pd.DataFrame(filter_mail(info),
                                            columns=['Tài khoản', 'Mật khẩu', 'Họ và tên', 'Ngày sinh', 'Số điện thoại',
                                                     'Email', 'Vị trí', 'Giới tính'])
                    st.write(filter_info)
            elif filter == 'Lọc theo giới tính':
                info = st.selectbox('',('Nam','Nữ'))
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    filter_info = pd.DataFrame(filter_sex(info),
                                            columns=['Tài khoản', 'Mật khẩu', 'Họ và tên', 'Ngày sinh', 'Số điện thoại',
                                                     'Email', 'Vị trí', 'Giới tính'])
                    st.write(filter_info)
            elif filter == 'Lọc theo vị trí':
                info = st.selectbox("Địa chỉ:", (
                "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Bến Tre", "Bình Định",
                "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cần Thơ", "Cao bằng", "Đà Nẵng", "Đắk Lắk",
                "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh",
                "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum",
                "Lai Châu",
                "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận",
                "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng",
                "Sơn La", "Tây Ninh",
                "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP. Hồ Chí Minh", "Trà Vinh",
                "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"))
                submit = st.form_submit_button("Xác nhận")
                if submit:
                    filter_info = pd.DataFrame(filter_address(info),
                                            columns=['Tài khoản', 'Mật khẩu', 'Họ và tên', 'Ngày sinh', 'Số điện thoại',
                                                     'Email', 'Vị trí', 'Giới tính'])
                    st.write(filter_info)

    elif task == "Thống kê chẩn đoán":
        col1, col2 = st.columns([7,3])
        with col1:
            st.subheader('KẾT QUẢ CHẨN ĐOÁN CỦA NGƯỜI DÙNG:')
            userinfo = pd.DataFrame(displayall_result(),
                                        columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
            st.dataframe(userinfo)
            #st.markdown("***")
            filter = st.selectbox("LỌC DỮ LIỆU:",
                                  ["Lọc theo tài khoản", "Lọc theo tên", "Lọc theo ngày sinh", "Lọc theo kết quả", "Lọc theo ngày chẩn đoán", 'Lọc theo giới tính', 'Lọc theo kết quả'])
            with st.form('form_filter'):
                if filter == 'Lọc theo tài khoản':
                    info = st.text_input('')
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        filter_info = pd.DataFrame(filter1_username(info),
                                                   columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
                        st.write(filter_info)
                elif filter == 'Lọc theo tên':
                    info = st.text_input('')
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        filter_info = pd.DataFrame(filter1_name(info),
                                                   columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
                        st.write(filter_info)
                elif filter == 'Lọc theo ngày sinh':
                    info = str(st.date_input("Ngày sinh: "))
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        filter_info = pd.DataFrame(filter1_age(info),
                                                   columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
                        st.write(filter_info)
                elif filter == 'Lọc theo ngày chẩn đoán':
                    info = str(st.date_input("Ngày sinh: "))
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        filter_info = pd.DataFrame(filter1_date(info),
                                                   columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
                        st.write(filter_info)
                elif filter == 'Lọc theo vị trí':
                    info = st.selectbox("Địa chỉ:", (
                        "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Bến Tre",
                        "Bình Định",
                        "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cần Thơ", "Cao bằng", "Đà Nẵng", "Đắk Lắk",
                        "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội",
                        "Hà Tĩnh",
                        "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang",
                        "Kon Tum",
                        "Lai Châu",
                        "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận",
                        "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị",
                        "Sóc Trăng",
                        "Sơn La", "Tây Ninh",
                        "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP. Hồ Chí Minh",
                        "Trà Vinh",
                        "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"))
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        filter_info = pd.DataFrame(filter1_address(info),
                                                   columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
                        st.write(filter_info)
                elif filter == 'Lọc theo giới tính':
                    info = st.selectbox('', ('Nam', 'Nữ'))
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        filter_info = pd.DataFrame(filter1_sex(info),
                                                   columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
                        st.write(filter_info)
                elif filter == 'Lọc theo kết quả':
                    info = st.selectbox('', ('Âm tính', 'Dương tính'))
                    if info == 'Âm tính':
                        info = 0
                    else:
                        info = 1
                    submit = st.form_submit_button("Xác nhận")
                    if submit:
                        filter_info = pd.DataFrame(filter1_result(info),
                                                   columns=['Tài khoàn sử dụng' ,'Kết quả', 'Tên bệnh nhân' , 'Ngày sinh', 'Địa chỉ', 'Giới tính', 'Tên tệp ảnh', 'Ngày chẩn đoán'])
                        st.write(filter_info)
        with col2:
            st.subheader('BIỂU ĐỒ:')
            labels = 'Âm tính', 'Dương tính'
            sizes = [count_data(0), count_data(1)]
            my_colors = ['green', 'red']
            plt.figure(figsize=plt.figaspect(1))
            wp = {'linewidth': 1, 'edgecolor': "black"}
            plt.pie(sizes, startangle=90, autopct=make_autopct(sizes),wedgeprops = wp, colors=my_colors)
            plt.legend(labels,
                      title="Kết quả chẩn đoán:",
                      loc="best")
            st.pyplot(plt)


def sign_gui():
    menu = st.sidebar.selectbox("MENU:",["Trang chủ","Đăng kí"])
    st.sidebar.markdown("***")
    if menu == "Trang chủ":
        username = st.sidebar.text_input("Tài khoản: ")
        password = st.sidebar.text_input("Mật khẩu: ",type='password')
        st.sidebar.markdown("***")
        if st.sidebar.button("Xác nhận") and st.session_state['login'] == 'notlogin':
            if username and password:
                result = login_user(username, password)
                if result and str(select(username, 0)) != "admin":
                    with st.sidebar:
                        with st.spinner("Đang xử lí..."):
                            time.sleep(0.5)
                            st.sidebar.success("Đăng nhập thành công!")
                            st.session_state['login'] = 'loginuser'
                            st.session_state['username'] = username
                            st.experimental_rerun()
                elif result and str(select(username, 0)) == "admin":
                    with st.sidebar:
                        with st.spinner("Đang xử lí..."):
                            time.sleep(0.5)
                            st.sidebar.success("Đăng nhập thành công!")
                            st.session_state['login'] = 'loginadmin'
                            st.experimental_rerun()
                else:
                    st.sidebar.error('Tài khoản hoặc mật khẩu không chính xác, xin thử lại !!!')
                    main_gui()
                    st.stop()
            else:
                st.sidebar.error('Vui lòng cung cấp đầy đủ tài khoản và mật khẩu !!!')
                main_gui()
                st.stop()
        else:
            main_gui()
            st.stop()
    elif menu == "Đăng kí":
        allowed_num = set(("0123456789"))
        allowed_chars = set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"))
        with st.sidebar:
            st.info('Thông tin đăng kí của bạn sẽ được bảo mật và lưu trữ ở cơ sở dữ liệu !')
        with st.form('form1'):
            st.header('Vui lòng điền đầy đủ thông tin đăng kí: 📋')
            st.markdown("***")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Họ và tên: ")
            with col2:
                age = st.date_input("Ngày sinh: ")
            col3, col4 = st.columns(2)
            with col3:
                phone = st.text_input("Số điện thoại: ")
                phone_set = set(phone)
            with col4:
                mail = st.text_input("Email: ")
            col8, col9 = st.columns(2)
            with col8:
                address = st.selectbox("Địa chỉ:",("An Giang","Bà Rịa - Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre","Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao bằng","Đà Nẵng","Đắk Lắk",
                                       "Đắk Nông","Điện Biên","Đồng Nai","Đồng Tháp","Gia Lai","Hà Giang","Hà Nam","Hà Nội","Hà Tĩnh","Hải Dương","Hải Phòng","Hậu Giang","Hòa Bình","Hưng Yên","Khánh Hòa","Kiên Giang","Kon Tum","Lai Châu",
                                       "Lâm Đồng","Lạng Sơn","Lào Cai","Long An","Nam Định","Nghệ An","Ninh Bình","Ninh Thuận","Phú Thọ","Phú Yên","Quảng Bình","Quảng Nam","Quảng Ngãi","Quảng Ninh","Quảng Trị","Sóc Trăng","Sơn La","Tây Ninh",
                                       "Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","TP. Hồ Chí Minh","Trà Vinh","Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái"))
            with col9:
                sex = st.selectbox("Giới tính", ["Nam","Nữ","Khác"])
            col5, none = st.columns(2)
            with col5:
                username_new = st.text_input("Tên tài khoản: ")
                username_new_set = set(username_new)
            col6, col7 = st.columns(2)
            with col6:
                password_new = st.text_input("Mật khẩu: ",type='password')
            with col7:
                password_repeat = st.text_input("Nhập lại mật khẩu: ",type='password')
            st.markdown("***")
            submit = st.form_submit_button("Xác nhận")
        if submit:
            if name and age and address and username_new and password_new and password_repeat and mail and phone and sex:
                if username_new_set.issubset(allowed_chars) and len(username_new) >4 and len(username_new) <15 and password_new == password_repeat and phone_set.issubset(allowed_num) and len(phone) == 10:
                    if check_username(username_new):
                        st.error('Tài khoản đã tồn tại, vui lòng thử tên tài khoản khác !')
                    else:
                        with st.spinner("Đang xử lí..."):
                            time.sleep(2)
                            create_usertable()
                            add_userdata(username_new, password_new, name, age, phone, mail, address, sex)
                            st.success("Đăng kí tài khoản mới thành công !")
                        time.sleep(0.5)
                        st.info("Mời bạn quay về trang chủ để đăng nhập và sử dụng")
                else:
                    if username_new_set.issubset(allowed_chars) == False or len(username_new) <5 or len(username_new) >15:
                        st.error('Tên tài khoản không hợp lệ ( độ dài 6 - 15 kí tự và không sử dụng kí tự đặc biệt ) !')
                    if password_new != password_repeat:
                        st.error('Nhập lại mật khẩu không chính xác !')
                    if phone_set.issubset(allowed_num) == False or len(phone) != 10:
                        st.error('Số điện thoại liên lạc không hợp lệ !')
            else:
                st.warning('Vui lòng cung cấp đầy đủ thông tin cần thiết !')

if __name__ == '__main__':
    if 'login' not in st.session_state:
        #publ_url = ngrok.connect()
        time.sleep(2)
        st.session_state['login'] = 'notlogin'
    if st.session_state['login'] == 'notlogin':
        sign_gui()
    elif st.session_state['login'] == 'loginuser':
        user_gui()
    else:
        admin_gui()
