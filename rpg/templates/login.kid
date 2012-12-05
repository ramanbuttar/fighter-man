<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>FighterMan - Login</title>
</head>

<body>
    <div id="loginBox" class="floatRight" >
        <p py:if="tg.identity.anonymous">${message}</p>
        <p py:if=" not tg.identity.anonymous">You are logged in as: <strong>${tg.identity.user.display_name}</strong> <a href="${tg.url('/logout')}">(Logout)</a></p>

        <form action="${tg.url(previous_url)}" method="POST">
            <table>
                <tr>
                    <td class="label">
                        <label for="user_name">User Name:</label>
                    </td>
                    <td class="field">
                        <input type="text" id="user_name" name="user_name"/>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        <label for="password">Password:</label>
                    </td>
                    <td class="field">
                        <input type="password" id="password" name="password"/>
                    </td>
                </tr>
                <tr>
                    <td colspan="2" class="buttons">
                        <input type="submit" name="login" value="Login"/>
                    </td>
                </tr>
            </table>

            <input py:if="forward_url" type="hidden" name="forward_url"
                value="${forward_url}"/>
                
            <div py:for="name,values in original_parameters.items()" py:strip="1">
            <input py:for="value in isinstance(values, list) and values or [values]"
                type="hidden" name="${name}" value="${value}"/>
            </div>
        </form>
    </div>
<h1>What is FighterMan?</h1>

<p>Fighter Man is a web-based Role Playing Game that allows users to assume the role of a general manager and be responsible for complete management of their prizefighter.</p>
<h1>How do I get started?</h1>
<p>To get started, <a href="${tg.url('/register')}">register</a> for a new account.</p>
</body>
</html>
