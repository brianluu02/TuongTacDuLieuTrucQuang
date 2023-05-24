import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from dash.dependencies import Input, Output
# Đọc dữ liệu từ file CSV
url = "https://raw.githubusercontent.com/YuehHanChen/Marketing_Analytics/main/marketing_data.csv"
df = pd.read_csv(url)

# Xử lý dữ liệu
df.columns = df.columns.str.replace(' ', '')
df['Income'] = df['Income'].replace({'\$': '', '\.': '', '00': '', ',': ''}, regex=True).astype(float)
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
df['Income'] = df['Income'].fillna(df['Income'].median())
df = df.drop(['ID', 'Marital_Status'], axis=1)
spending_cols = ['MntFishProducts', 'MntMeatProducts', 'MntFruits', 'MntSweetProducts', 'MntWines', 'MntGoldProds']
# thông tin về số tiền khách hàng đã chi tiêu cho các loại sản phẩm, gồm đồ hải sản (MntFishProducts), thịt (MntMeatProducts), hoa quả (MntFruits), đồ ngọt (MntSweetProducts), rượu vang (MntWines) và vàng (MntGoldProds).
df['MntSpent'] = df[spending_cols].sum(axis=1)
# tổng số tiền mà mỗi khách hàng đã chi tiêu cho các loại sản phẩm nêu trên và lưu vào cột mới MntSpent
purchases_cols = ['NumCatalogPurchases', 'NumStorePurchases', 'NumWebPurchases'] 
# thông tin về số lần mua hàng của khách hàng từ các kênh bán hàng khác nhau, gồm mua trực tiếp tại cửa hàng (NumStorePurchases), mua hàng qua web (NumWebPurchases) và mua hàng qua catalogue (NumCatalogPurchases).
df['NumPurchases'] = df[purchases_cols].sum(axis=1)
# tính tổng số lần mua hàng của mỗi khách hàng từ các kênh bán hàng nêu trên và lưu vào cột mới NumPurchases.
kid_cols = ['Kidhome', 'Teenhome']
df['TotalKid'] = df[kid_cols].sum(axis=1)
#tính tổng số lượng trẻ em trong gia đình mỗi khách hàng từ 1 đến 18 tuổi và lưu vào cột mới TotalKid
accepted_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
df['TotalAccepted'] = df[accepted_cols].sum(axis=1)
# Dòng này tính tổng số lượng cảnh báo quảng cáo hoặc chương trình khuyến mãi mà mỗi khách hàng và lưu vào cột mới TotalAccepted.

#  Xử lý ngoại lệ 
Q1 = df['Income'].quantile(0.25)
Q3 = df['Income'].quantile(0.75)
IQR = Q3 - Q1
#Xóa các giá trị ngoại lệ trong cột Income
df = df[~((df['Income'] < (Q1 - 1.5 * IQR)) | (df['Income'] > (Q3 + 1.5 * IQR)))]

df['Age'] = 2022 - df['Year_Birth']

# TẠO VÀ VẼ BIỂU ĐỒ #


# Tạo biểu đồ tròn (pie chart) hiển thị tỷ lệ phân loại học vấn của khách hàng
fig1 = px.pie(df, names='Education', title='Tỉ lệ phân loại học vấn của khách hàng')
# Tạo biểu đồ cột (bar chart) hiển thị số lượng sản phẩm được mua theo từng danh mục
fig2 = px.bar(df, x='Country', y=['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'], title='Tổng quan về số lượng sản phẩm được mua theo danh mục tại các vùng')

# Tạo biểu đồ scatter plot hiển thị mối quan hệ giữa thu nhập và chi phí cho các sản phẩm khác nhau
fig3 = px.scatter(df, x='Income', y='MntWines', color='Country', size='MntFruits',
                 hover_data=['Education', 'Income'], title='Từng vùng địa lý có thể ảnh hưởng đến cách khách hàng chọn lựa giữa mua rượu vang và trái cây, dựa trên thu nhập của họ',
                 labels={'Income': 'Thu nhập', 'MntWines': 'Số lần mua rượu vang'})


# Tính toán tỷ lệ chấp nhận các chiến dịch tiếp thị theo từng khu vực
df_acceptance_rate = df.groupby(['Country'])[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']].mean().reset_index()

attributes = ['Education', 'Income',
            'MntSpent', 'NumPurchases', 'Country']

# Biểu đồ boxplot được 
box_fig = px.box(df, y='Income', color='Education')
# Create grid of selection
grid_fig = px.scatter_matrix(df[attributes], dimensions=attributes, color='Country')

# Dữ liệu tiền xử lý để tính giá trị trung bình của cột Income cột by Country
df_agg = df.groupby(['Country']).agg({'Income': 'mean'}).reset_index()
# Tạo DataFrame mới chỉ lấy cột Age và Income
df_income = df[['Age', 'Income']]

# Groupby theo Age và tính trung bình Income trong mỗi nhóm
df_income_avg = df_income.groupby('Age').mean()

# Vẽ biểu đồ đường thống kê
fig4 = go.Figure()

# Thêm trace cho các điểm dữ liệu
fig4.add_trace(go.Scatter(x=df_income_avg.index, y=df_income_avg['Income'], mode='markers', name='Thu nhâp'))

# Thêm trace cho đường trung bình
fig4.add_trace(go.Scatter(x=df_income_avg.index, y=df_income_avg['Income'], mode='lines', name='Đường trung bình'))

# Thêm layout cho biểu đồ
fig4.update_layout(title="Đường trung bình thu nhập theo tuổi",
                   xaxis_title="Tuổi",
                   yaxis_title="Thu nhập trung bình")
# Tạo DataFrame mới chỉ lấy cột Country và các cột tham chiếu số lượng sản phẩm
df_products = df[['Country', 'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']]


# thống kê 
## Tạo DataFrame mới chỉ lấy các thuộc tính quan trọng
df_target = df[['Age', 'Education','MntFishProducts', 'Income', 'MntWines', 'Country','AcceptedCmp3', 'TotalKid']]

# Tính toán giá trị trung bình của Income và MntWines theo từng quốc gia
df_target_avg = df_target.groupby('Country').mean(numeric_only=True).reset_index()


fig5 = px.scatter(df_target_avg, x='Income', y='MntWines', color='Country',
                 hover_data=['Country'], title='Biểu đồ scatter plot cho Income và MntFishProducts')

# Thêm đường thống kê mục tiêu
fig5.add_trace(go.Scatter(x=[0, 250000], y=[0, 1500], mode='lines', name='Mục tiêu'))
fig5.update_layout(title="Mối quan hệ giữa thu nhập trung bình và số lần mua rượu vang theo vùng",
                   xaxis_title="Thu nhập trung bình",
                   yaxis_title="Số lần mua rượu vang")
# thêm css và html cho code trong đẹp hơn 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Tạo ứng dụng Dash và kết nối với CSS stylesheet
Nhom5_Report = dash.Dash(__name__, external_stylesheets=external_stylesheets)

Nhom5_Report.layout = html.Div(children=[
    # Thêm tiêu đề cho ứng dụng
    html.H1(children='Đề tài: PHÂN TÍCH DỮ LIỆU VÀ XÂY DỰNG DASHBOARD TỪ DỮ LIỆU MARKETING ANALYST BẰNG PYTHON DASH PLOTLY WEB APPLICATION',style={'textAlign': 'center','font-weight': 'bold'}),
    html.H1(style={
    'font-size': '36px',
    'text-align': 'left',
}, children=[
    html.Span(style={'color': '#000000', 'font-weight': 'bold', 'margin-right': '10px','font-size': '36px'}, children='Giảng Viên Hướng Dẫn'),
    html.Span(style={'font-weight': 'bold','font-size': '36px'}, children=': ThS. Lê Minh Tân'),
    html.Br(),
    html.Span(style={'color': '#000000'}, children='01.'),
    html.Span('Phan Quốc Lưu'),
    html.Span(style={'font-size': '36px', 'margin-left': '10px'}, children='- 20133065'),
    html.Br(),
    html.Span(style={'color': '#000000'}, children='02.'),
    html.Span('Cao Trọng Nghĩa'),
    html.Span(style={'font-size': '36px', 'margin-left': '10px'}, children='- 20133071'),
  
]),
    html.Label('Nhập số tuổi:', style={'font-weight': 'bold','font-size': '16px'}),
    dcc.Input(
        id='input-year',
        type='number',  
        value='',
        style={'width': '10%'}
    ),

    # Thêm trường chọn dropdown cho trình độ học vấn
    html.Br(),
    html.Label('Chọn trình độ học vấn:', style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id='dropdown-education',
        options=[
            {'label': 'Graduation', 'value': 'Graduation'},
            {'label': '2n Cycle', 'value': '2n Cycle'},
            {'label': 'Basic', 'value': 'Basic'},
            {'label': 'Master', 'value': 'Master'},
            {'label': 'PhD', 'value': 'PhD'}
        ],
        value='Graduation',
        style={'width': '38%'}
    ),


    # Biểu đồ tròn hiển thị tỷ lệ số lượng trẻ em và số lượng sản phẩm đã mua
    dcc.Graph(id='pie-chart'),

    # Biểu đồ scatter plot hiển thị tổng chi tiêu của khách hàng theo thu nhập và trình độ học vấn
    dcc.Graph(id='scatter-plot'),
    # Thêm biểu đồ tròn
    dcc.Graph(
        id='pie-chart1',
        figure=fig1
    ),

    # Thêm biểu đồ cột
    dcc.Graph(
        id='bar-chart',
        figure=fig2
    ),
    dcc.Graph(
        id='scatter-plot1',
        figure=fig3
    ),
    dcc.Graph(
    id='bar-chart-2',
    figure=px.bar(df_acceptance_rate, x='Country', y=['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5'], barmode='group')
        .update_layout(title='Biểu đồ so sánh tỉ lệ chấp nhận chiến dịch tiếp thị theo vùng')
    ),
    html.H3('Biểu đồ nâng cao'),
    dcc.Tabs([
        dcc.Tab(label='Thu nhập của khách hàng dựa trên trình độ học vấn', children=[
            html.Div([
                dcc.Graph(figure=box_fig),
            ])
        ]),
        dcc.Tab(label='Tương quan giữa các thuộc tính khách hàng', children=[
            html.Div([
                dcc.Graph(figure=grid_fig),
            ])
        ]),
    ]),
    
    dcc.Graph(id='line-chart', figure=fig4),
    dcc.Graph(id='scatter-plot2', figure=fig5)
])

# Định nghĩa callback để cập nhật biểu đồ tròn
@Nhom5_Report.callback(
    Output('pie-chart', 'figure'),
    Input('input-year', 'value')
)
def update_pie_chart(year):
    if year is None or (year < df['Age'].min() or year > df['Age'].max()):
        raise dash.exceptions.PreventUpdate
    # Lọc dữ liệu theo năm sinh
    filtered_df = df[df['Age'] == year]

    # Tính tỷ lệ số lượng trẻ em và số lượng sản phẩm đã mua
    kidhome_percent = len(filtered_df[filtered_df['TotalKid'] == 1]) / len(filtered_df) * 100
    # Hàm tính tỷ lệ khách hàng có trẻ em (TotalKid = 1) trong tập dữ liệu đã lọc và gán kết quả vào biến kidhome_percent. Nếu không có khách hàng nào có trẻ em, tỷ lệ này sẽ là 0.
    product_spent_percent = len(filtered_df[filtered_df['MntSpent'] > 0]) / len(filtered_df) * 100
    # Hàm tính tỷ lệ khách hàng đã mua sản phẩm (MntSpent > 0) trong tập dữ liệu đã lọc và gán kết quả vào biến product_spent_percent.
    if kidhome_percent == 0:
        pie_chart = px.pie(
        values=[1, product_spent_percent],
        names=["Khách hàng không có trẻ em", "Tổng số tiền mà mỗi khách hàng đã chi tiêu cho các loại sản phẩm"],
        title="Tỷ lệ khách hàng có trẻ em và Tổng số tiền mà mỗi khách hàng đã chi tiêu cho các loại sản phẩm"
    )
    else:
        pie_chart = px.pie(
        values=[kidhome_percent, product_spent_percent],
        names=["Khách hàng có trẻ em", "Tổng số tiền mà mỗi khách hàng đã chi tiêu cho các loại sản phẩm"],
        title="Tỷ lệ khách hàng có trẻ em và Tổng số tiền mà mỗi khách hàng đã chi tiêu cho các loại sản phẩm"
    )

    return pie_chart


# Định nghĩa callback để cập nhật biểu đồ scatter plot
@Nhom5_Report.callback(
    Output('scatter-plot', 'figure'),
    Input('dropdown-education', 'value')
)
def update_scatter_plot(education):
    # Lọc dữ liệu theo trình độ học vấn
    filtered_df = df[df['Education'] == education]

    # Tạo biểu đồ scatter plot
    scatter_plot = px.scatter(
        filtered_df,
        x='Income',
        y='MntSpent',
        color='Education',
        hover_data=['Dt_Customer'],
        title="Tương quan giữa thu nhập và mức chi tiêu cá nhân theo trình độ học vấn"
    )
    return scatter_plot

if __name__ == '__main__':
    Nhom5_Report.run_server(debug=True)
