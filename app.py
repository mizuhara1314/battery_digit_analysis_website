from flask import Flask,render_template,request,redirect,url_for,Response
import pandas as pd
import All
app = Flask(__name__)
All.generator_graph()


@app.route('/')
def xyz():
    return render_template("index.html")

@app.route('/generate_chart',methods=["POST"])
def index():
    img="img"
    if request.method == 'POST':
            
            chart_type = request.form.get('chart')

            if chart_type == '生成充电容量与电压图':
                img="img2/a.png"
                
                # 执行生成充电容量与电压图的逻辑
                pass
            elif chart_type == '生成放电容量与电流图':
                img="img2/b.png"
                # 执行生成放电容量与电流图的逻辑
                pass
            elif chart_type == '生成充电容量与温度图':
                img="img2/c.png"
                # 执行生成充电容量与温度图的逻辑
                pass
            elif chart_type == '生成容量衰减曲线图':
                img="img2/d.png"
                # 执行生成容量衰减曲线图的逻辑
                pass
            elif chart_type == '生成累积容量曲线图':
                img="img2/e.png"
                # 执行生成累积容量曲线图的逻辑
                pass
            elif chart_type == '生成累积容量与总电压曲线图':
                img="img2/f.png"
                # 执行生成累积容量与总电压曲线图的逻辑
                pass
            elif chart_type == '生成dQ/dV曲线图':
                image_files = [f'img2/{i}.png' for i in range(1, 5)]
                return render_template('result3.html', images=image_files)
                pass
            elif chart_type == '生成描述性统计信息':
                df=pd.read_csv("static/descriptive_stats.csv")
                df_values = df.values.tolist()
                df_columns = df.columns.tolist()
                return render_template('result2.html', columns=df_columns, data=df_values)
                # 执行生成描述性统计信息的逻辑
                pass
            elif chart_type == '生成相关性分析热图':
                img="img2/h.png"
                # 执行生成相关性分析热图的逻辑
                pass
            elif chart_type == '生成参数关系图':
                img="img2/g.png"
                # 执行生成参数关系图的逻辑
                pass
            else:
                # 未知的图表类型
                pass

    
    return render_template("result.html",img_url=img)



if __name__ == '__main__':
    app.run(debug=True, port=7000)


