import asyncio
import random
import io

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    BufferedInputFile,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.filters import Command
from sympy import sin, cos, diff, symbols, integrate, sqrt, pi, simplify, solve, Abs, latex as sp_latex
from sympy.abc import x as sym_x, y as sym_y

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_sessions: dict[int, dict] = {}

x, y = symbols("x y", real=True)


def latex_to_image(latex_str: str) -> io.BytesIO:
    """LaTeX формуласын PNG суретке айналдырады."""
    fig = plt.figure(figsize=(8, 1.2))
    fig.patch.set_facecolor('white')
    
    plt.axis('off')
    plt.text(
        0.5, 0.5, f"${latex_str}$",
        fontsize=20,
        ha='center', va='center',
        color='black'
    )
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf


def gen_derivative():
    """Туынды есебі - кездейсоқ параметрлермен"""
    a = random.randint(1, 5)
    k = random.choice([3, 4, 6])
    c = random.randint(1, 8)
    
    task_text = f"Туындысын табыңыз:"
    task_latex = f"y = \\sin({a}x + \\frac{{\\pi}}{{{k}}}) + {c}"
    
    # Дұрыс жауапты есептейміз
    func = sin(a*x + pi/k) + c
    derivative = diff(func, x)
    answer_text = str(derivative).replace("**", "^").replace("*", "·")
    answer_latex = sp_latex(derivative)
    
    # Қате жауаптар
    wrong1 = str(a * sin(a*x + pi/k)).replace("**", "^").replace("*", "·")
    wrong2 = str(cos(a*x + pi/k)).replace("**", "^").replace("*", "·")
    wrong3 = str((a+1) * cos(a*x + pi/k)).replace("**", "^").replace("*", "·")
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_root_factor():
    """Түбірден көбейткіш шығару - кездейсоқ параметрлермен"""
    coef = random.choice([12, 18, 27, 32, 48, 50, 75, 98, 108, 128])
    px = random.choice([2, 3, 4, 5, 6])
    py = random.choice([1, 2, 3, 4, 5])
    
    task_text = f"Көбейткішті түбір белгісінің алдына шығарыңыз:"
    task_latex = f"\\sqrt{{{coef}x^{{{px}}}y^{{{py}}}}}"
    
    # SymPy арқылы қарапайымдандыру
    from sympy import sqrt, simplify, latex as sp_latex
    expr = sqrt(coef * x**px * y**py)
    simplified = simplify(expr)
    
    answer_text = str(simplified).replace("**", "^").replace("*", "·")
    answer_latex = sp_latex(simplified)
    
    # Қате жауаптар
    out_coef = int(coef**0.5) if int(coef**0.5)**2 == coef else int(coef**0.5) + 1
    wrong1 = f"{out_coef}·x^{px//2}·y^{py//2}"
    wrong2 = f"√{coef}·x^{px}·y^{py}"
    wrong3 = f"{out_coef+1}·x^{px//2}·y^{py//2}"
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_arcsin():
    """arcsin теңдеуі - кездейсоқ параметрлермен"""
    angle = random.choice([pi/6, pi/4, pi/3])
    angle_str = {pi/6: "\\frac{\\pi}{6}", pi/4: "\\frac{\\pi}{4}", pi/3: "\\frac{\\pi}{3}"}[angle]
    
    task_text = f"Теңдеуді шешіңіз:"
    task_latex = f"\\arcsin(2x) = {angle_str}"
    
    # Дұрыс жауапты есептейміз: arcsin(2x) = angle => 2x = sin(angle) => x = sin(angle)/2
    sin_val = sin(angle)
    x_val = sin_val / 2
    
    answer_text = f"x = {sp_latex(x_val)}"
    answer_latex = f"x = {sp_latex(x_val)}"
    
    # Қате жауаптар
    wrong1 = f"x = {sp_latex(sin_val)}"
    wrong2 = f"x = {sp_latex(2*sin_val)}"
    wrong3 = f"x = {angle_str}"
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_domain():
    """Анықталу облысы - кездейсоқ параметрлермен"""
    shift = random.randint(1, 10)
    
    task_text = f"Анықталу облысын табыңыз:"
    task_latex = f"y = e^{{\\sqrt{{x - {shift}}}}}"
    
    answer_text = f"x ≥ {shift}"
    answer_latex = f"x \\geq {shift}"
    
    wrong1 = f"x > {shift}"
    wrong2 = f"x ≤ {shift}"
    wrong3 = f"x ≥ {shift+1}"
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_integral():
    """Интеграл - кездейсоқ параметрлермен"""
    n = random.randint(2, 6)
    upper = random.randint(2, 5)
    
    task_text = f"Интегралды есептеңіз:"
    task_latex = f"\\int_0^{{{upper}}} x^{{{n}}} \\, dx"
    
    # Дұрыс жауапты есептейміз
    from sympy import integrate
    result = integrate(x**n, (x, 0, upper))
    
    answer_text = str(result)
    answer_latex = sp_latex(result)
    
    # Қате жауаптар
    wrong1 = str(upper**(n+1) // (n+2))
    wrong2 = str(upper**n)
    wrong3 = str(upper**(n+1))
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_7_system():
    """Көрсеткіштік теңдеулер жүйесі - кездейсоқ параметрлермен"""
    # Базаны өзгертеміз
    base = random.choice([5, 7, 11])
    sum_exp = random.randint(3, 5)  # x + y
    
    # x + y = sum_exp деп қабылдап, 7^x + 7^y мәнін есептейміз
    # Мысалы: x=1, y=sum_exp-1 немесе x=2, y=sum_exp-2
    x_val = random.randint(1, sum_exp-1)
    y_val = sum_exp - x_val
    
    sum_powers = base**x_val + base**y_val
    product_val = 2 * base**sum_exp
    
    task_text = "Жүйені шешіңіз:"
    task_latex = f"\\begin{{cases}} {base}^x + {base}^y = {sum_powers} \\\\ 2 \\cdot {base}^{{x+y}} = {product_val} \\end{{cases}}"
    
    answer_text = f"({x_val}, {y_val}) немесе ({y_val}, {x_val})"
    answer_latex = f"(x, y) \\in \\{{({x_val}, {y_val}), ({y_val}, {x_val})\\}}"
    
    wrong1 = f"({x_val+1}, {y_val-1})"
    wrong2 = f"({sum_exp//2}, {sum_exp//2})"
    wrong3 = f"({x_val}, {y_val+1})"
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_gp():
    """Геометриялық прогрессия - кездейсоқ параметрлермен"""
    q = random.choice([2, 3, 4])  # еселік
    b1 = random.randint(2, 10)
    
    # b_n = b1 * q^(n-1)
    b4 = b1 * q**3
    sum_b1_b4 = b1 + b4
    
    b2 = b1 * q
    b3 = b1 * q**2
    product_b2_b3 = b2 * b3
    
    task_text = f"Геометриялық прогрессияның еселігін табыңыз:"
    task_latex = f"b_1 + b_4 = {sum_b1_b4}, \\quad b_2 \\cdot b_3 = {product_b2_b3}"
    
    answer_text = f"q = {q}"
    answer_latex = f"q = {q}"
    
    wrong1 = f"q = {q+1}"
    wrong2 = f"q = {q-1 if q > 2 else q+2}"
    wrong3 = f"q = {q*2}"
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_distance():
    """Нүктеден жазықтыққа қашықтық - кездейсоқ параметрлермен"""
    # Нүкте
    x0, y0, z0 = random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5)
    
    # Жазықтық: Ax + By + Cz + D = 0
    A, B, C = random.randint(1, 5), random.randint(1, 5), random.randint(-5, 5)
    D = random.randint(-10, 10)
    
    task_text = f"Нүктеден жазықтыққа дейінгі қашықтықты табыңыз:"
    task_latex = f"A({x0}; {y0}; {z0}), \\quad {A}x + {B}y + {C}z + {D} = 0"
    
    # Формула: d = |Ax0 + By0 + Cz0 + D| / sqrt(A^2 + B^2 + C^2)
    from sympy import Abs, sqrt, simplify
    numerator = abs(A*x0 + B*y0 + C*z0 + D)
    denominator = sqrt(A**2 + B**2 + C**2)
    distance = simplify(numerator / denominator)
    
    answer_text = str(distance).replace("**", "^").replace("*", "·")
    answer_latex = sp_latex(distance)
    
    wrong1 = str(numerator)
    wrong2 = str(float(distance) + 1)[:5]
    wrong3 = str(float(distance) - 1)[:5]
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_abs_power():
    """Модульді дәреже теңдеуі - кездейсоқ параметрлермен"""
    center = random.randint(3, 8)
    
    task_text = f"Түбірлердің қосындысын табыңыз:"
    task_latex = f"|{center} - x|^{{x + 1}} = 1"
    
    # |center - x|^(x+1) = 1
    # Шешімдер: |center-x|=1 => x=center±1, немесе x+1=0 => x=-1
    roots = [center-1, center+1, -1]
    sum_roots = sum(roots)
    
    answer_text = str(sum_roots)
    answer_latex = str(sum_roots)
    
    wrong1 = str(sum_roots + 1)
    wrong2 = str(sum_roots - 1)
    wrong3 = str(center + center-1)
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def gen_quadratic():
    """Квадрат теңдеу - кездейсоқ параметрлермен"""
    # ax^2 + bx + c = 0
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    
    task_text = f"Квадрат теңдеудің түбірлерін табыңыз:"
    task_latex = f"{a}x^2 + {b}x + {c} = 0"
    
    # Дискриминант
    from sympy import solve
    solutions = solve(a*x**2 + b*x + c, x)
    
    if len(solutions) == 0:
        answer_text = "Шешімі жоқ"
        answer_latex = "\\text{Шешімі жоқ}"
    elif len(solutions) == 1:
        answer_text = f"x = {sp_latex(solutions[0])}"
        answer_latex = f"x = {sp_latex(solutions[0])}"
    else:
        answer_text = f"x₁ = {sp_latex(solutions[0])}, x₂ = {sp_latex(solutions[1])}"
        answer_latex = f"x_1 = {sp_latex(solutions[0])}, \\quad x_2 = {sp_latex(solutions[1])}"
    
    wrong1 = f"x = {random.randint(-5, 5)}"
    wrong2 = f"x = {random.randint(-5, 5)}"
    wrong3 = "Шешімі жоқ" if len(solutions) > 0 else f"x = {random.randint(-5, 5)}"
    
    return task_text, task_latex, answer_text, answer_latex, [wrong1, wrong2, wrong3]


def generate_random_task():
    """Кездейсоқ есеп генерациялайды және жауабын есептейді"""
    generators = [
        gen_derivative,
        gen_root_factor,
        gen_arcsin,
        gen_domain,
        gen_integral,
        gen_7_system,
        gen_gp,
        gen_distance,
        gen_abs_power,
        gen_quadratic,
    ]
    
    generator = random.choice(generators)
    task_text, task_latex, answer_text, answer_latex, wrong_answers = generator()
    
    # 4 нұсқа жасау: 1 дұрыс + 3 қате
    all_options = [answer_text] + wrong_answers
    random.shuffle(all_options)
    correct_index = all_options.index(answer_text) + 1  # 1-4 аралығында
    
    return task_text, task_latex, answer_text, answer_latex, all_options, correct_index


@dp.message(Command("start"))
async def start_handler(message: Message):
    intro_text = (
        "🎓 <b>ЕНТ Математика Тренажеры</b>\n\n"
        "Сәлем! Мен сізге ЕНТ-ға дайындалуға көмектесемін.\n\n"
        "🔹 Шексіз есептер кездейсоқ параметрлермен\n"
        "🔹 Әрбір есеп LaTeX форматында көрінеді\n"
        "🔹 4 жауап нұсқасынан дұрысын таңдаңыз\n\n"
        "Жаттығу бастайық! 💪"
    )
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📘 Жаңа есеп генерациялау")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(intro_text, parse_mode="HTML", reply_markup=keyboard)


@dp.message(F.text == "📘 Жаңа есеп генерациялау")
async def generate_task_handler(message: Message):
    user_id = message.from_user.id
    
    task_text, task_latex, answer_text, answer_latex, options, correct_index = generate_random_task()
    
    user_sessions[user_id] = {
        "correct_answer": answer_text,
        "answer_latex": answer_latex,
        "correct_index": correct_index
    }
    
    await message.answer("⏳ Есеп дайындалуда...")
    
    img_buf = latex_to_image(task_latex)
    photo = BufferedInputFile(img_buf.read(), filename="task.png")
    
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"A) {options[0]}", callback_data="option_1")],
            [InlineKeyboardButton(text=f"B) {options[1]}", callback_data="option_2")],
            [InlineKeyboardButton(text=f"C) {options[2]}", callback_data="option_3")],
            [InlineKeyboardButton(text=f"D) {options[3]}", callback_data="option_4")],
            [InlineKeyboardButton(text="🔄 Тағы генерациялау", callback_data="generate_new")]
        ]
    )
    
    caption = f"<b>📝 {task_text}</b>"
    
    await message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="HTML",
        reply_markup=inline_keyboard
    )


@dp.callback_query(F.data.startswith("option_"))
async def check_option(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    if user_id not in user_sessions:
        await callback_query.answer("⚠️ Алдымен есеп генерациялаңыз!")
        return
    
    selected = int(callback_query.data.split("_")[1])
    correct = user_sessions[user_id]["correct_index"]
    
    if selected == correct:
        answer_latex = user_sessions[user_id]["answer_latex"]
        answer_text = user_sessions[user_id]["correct_answer"]
        
        img_buf = latex_to_image(answer_latex)
        photo = BufferedInputFile(img_buf.read(), filename="answer.png")
        
        caption = f"<b>✅ Дұрыс жауап!</b>\n\n{answer_text}"
        
        await callback_query.message.answer_photo(
            photo=photo,
            caption=caption,
            parse_mode="HTML"
        )
        await callback_query.answer("✅ Дұрыс!", show_alert=False)
    else:
        await callback_query.answer(f"❌ Қате! Дұрыс жауап: {chr(64 + correct)}", show_alert=True)


@dp.callback_query(F.data == "generate_new")
async def generate_new_from_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    task_text, task_latex, answer_text, answer_latex, options, correct_index = generate_random_task()
    
    user_sessions[user_id] = {
        "correct_answer": answer_text,
        "answer_latex": answer_latex,
        "correct_index": correct_index
    }
    
    await callback_query.message.answer("⏳ Жаңа есеп дайындалуда...")
    
    img_buf = latex_to_image(task_latex)
    photo = BufferedInputFile(img_buf.read(), filename="task.png")
    
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"A) {options[0]}", callback_data="option_1")],
            [InlineKeyboardButton(text=f"B) {options[1]}", callback_data="option_2")],
            [InlineKeyboardButton(text=f"C) {options[2]}", callback_data="option_3")],
            [InlineKeyboardButton(text=f"D) {options[3]}", callback_data="option_4")],
            [InlineKeyboardButton(text="🔄 Тағы генерациялау", callback_data="generate_new")]
        ]
    )
    
    caption = f"<b>📝 {task_text}</b>"
    
    await callback_query.message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="HTML",
        reply_markup=inline_keyboard
    )
    
    await callback_query.answer()


if __name__ == "__main__":
    print("🚀 Бот іске қосылуда...")
    asyncio.run(dp.start_polling(bot))
