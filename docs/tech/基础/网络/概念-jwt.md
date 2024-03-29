# JWT基本知识

from https://www.jianshu.com/p/576dbf44b2ae

Json Web Toke（JWT），是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准RFC7519。JWT一般可以用作独立的身份验证令牌，可以包含用户标识、用户角色和权限等信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，特别适用于分布式站点的登录场景。
如上面的例子所示，JWT就是一个字符串，由三部分构成：

Header（头部）

Payload（数据）

Signature（签名）

- JWT 默认是不加密，不能将秘密数据写入 JWT。

- JWT 不仅可以用于认证，也可以用于交换信息。有效使用 JWT，可以降低服务器查询数据库的次数。JWT的安全特3. 

- JWT 本身包含了认证信息，一旦泄露，任何人都可以获得该令牌的所有权限。为了减少盗用，JWT 的有效期应该设置得比较短。对于一些比较重要的权限，使用时应该再次对用户进行认证。

- 为了减少盗用，JWT 不应该使用 HTTP 协议明码传输，要使用HTTPS 协议传输。

- JWT 的最大缺点是，由于服务器不保存 session 状态，因此无法在使用过程中废止某个 token，或者更改 token 的权限。也就是说，一旦 JWT 签发了，在到期之前就会始终有效，除非服务器部署额外的逻辑。


什么是JWT
Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。

起源
说起JWT，我们应该来谈一谈基于token的认证和传统的session认证的区别。

传统的session认证
我们知道，http协议本身是一种无状态的协议，而这就意味着如果用户向我们的应用提供了用户名和密码来进行用户认证，那么下一次请求时，用户还要再一次进行用户认证才行，因为根据http协议，我们并不能知道是哪个用户发出的请求，所以为了让我们的应用能识别是哪个用户发出的请求，我们只能在服务器存储一份用户登录的信息，这份登录信息会在响应时传递给浏览器，告诉其保存为cookie,以便下次请求时发送给我们的应用，这样我们的应用就能识别请求来自哪个用户了,这就是传统的基于session认证。

但是这种基于session的认证使应用本身很难得到扩展，随着不同客户端用户的增加，独立的服务器已无法承载更多的用户，而这时候基于session认证应用的问题就会暴露出来.

基于session认证所显露的问题
Session: 每个用户经过我们的应用认证之后，我们的应用都要在服务端做一次记录，以方便用户下次请求的鉴别，通常而言session都是保存在内存中，而随着认证用户的增多，服务端的开销会明显增大。

扩展性: 用户认证之后，服务端做认证记录，如果认证的记录被保存在内存中的话，这意味着用户下次请求还必须要请求在这台服务器上,这样才能拿到授权的资源，这样在分布式的应用上，相应的限制了负载均衡器的能力。这也意味着限制了应用的扩展能力。

CSRF: 因为是基于cookie来进行用户识别的, cookie如果被截获，用户就会很容易受到跨站请求伪造的攻击。

基于token的鉴权机制
基于token的鉴权机制类似于http协议也是无状态的，它不需要在服务端去保留用户的认证信息或者会话信息。这就意味着基于token认证机制的应用不需要去考虑用户在哪一台服务器登录了，这就为应用的扩展提供了便利。

流程上是这样的：

用户使用用户名密码来请求服务器
服务器进行验证用户的信息
服务器通过验证发送给用户一个token
客户端存储token，并在每次请求时附送上这个token值
服务端验证token值，并返回数据
这个token必须要在每次请求时传递给服务端，它应该保存在请求头里， 另外，服务端要支持CORS(跨来源资源共享)策略，一般我们在服务端这么做就可以了Access-Control-Allow-Origin: *。

那么我们现在回到JWT的主题上。

JWT长什么样？
JWT是由三段信息构成的，将这三段信息文本用.链接一起就构成了Jwt字符串。就像这样:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
JWT的构成
第一部分我们称它为头部（header),第二部分我们称其为载荷（payload, 类似于飞机上承载的物品)，第三部分是签证（signature).

header
jwt的头部承载两部分信息：

声明类型，这里是jwt
声明加密的算法 通常直接使用 HMAC SHA256
完整的头部就像下面这样的JSON：

{
  'typ': 'JWT',
  'alg': 'HS256'
}
然后将头部进行base64加密（该加密是可以对称解密的),构成了第一部分.

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
playload
载荷就是存放有效信息的地方。这个名字像是特指飞机上承载的货品，这些有效信息包含三个部分

标准中注册的声明
公共的声明
私有的声明
标准中注册的声明 (建议但不强制使用) ：

iss: jwt签发者
sub: jwt所面向的用户
aud: 接收jwt的一方
exp: jwt的过期时间，这个过期时间必须要大于签发时间
nbf: 定义在什么时间之前，该jwt都是不可用的.
iat: jwt的签发时间
jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。
公共的声明 ：
公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.

私有的声明 ：
私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。

定义一个payload:

{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}

然后将其进行base64加密，得到Jwt的第二部分。

eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9
signature
jwt的第三部分是一个签证信息，这个签证信息由三部分组成：

header (base64后的)
payload (base64后的)
secret
这个部分需要base64加密后的header和base64加密后的payload使用.连接组成的字符串，然后通过header中声明的加密方式进行加盐secret组合加密，然后就构成了jwt的第三部分。

// javascript
var encodedString = base64UrlEncode(header) + '.' + base64UrlEncode(payload);

var signature = HMACSHA256(encodedString, 'secret'); // TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
将这三部分用.连接成一个完整的字符串,构成了最终的jwt:

  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
注意：secret是保存在服务器端的，jwt的签发生成也是在服务器端的，secret就是用来进行jwt的签发和jwt的验证，所以，它就是你服务端的私钥，在任何场景都不应该流露出去。一旦客户端得知这个secret, 那就意味着客户端是可以自我签发jwt了。

如何应用
一般是在请求头里加入Authorization，并加上Bearer标注：

fetch('api/user/1', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
服务端会验证token，如果验证通过就会返回相应的资源。整个流程就是这样的:

## 优缺点

使用方法：一般是登录成功后后端生成jwt给前端，前端存储起来，后续请求将它放入HTTP请求的Header Authorization字段中。

### 优点

- 无状态，适合分布式应用；
- 自身包含身份验证所需信息，使得后端不用存储Session 信息。
- 对移动端APP友好

### 缺点

- token无法主动失效
由于 token 的无状态设计，导致了它最大的缺点：当后端在token 有效期内废弃一个 token 或者更改它的权限的话，不会立即生效，一般需要等到有效期过后才真正的废除掉这个token。另外，当用户 Logout 的话，token 也还有效。除非，我们在后端增加额外的处理逻辑，比如设置存储token黑名单，或者只允许白名单的token操作。

- token无法自动续期
由于实际项目中，token的有效期时间不宜设置过长，但是项目经理又要求在一定时间内（大于token的有效期）用户免登陆。这种场景下，jwt就无法完成token的自动刷新，因为token失效后需要重新登录去重新生成一个新的token， token的有效期无法自动延长。除非给每个请求重新下发新的token或者token过期了直接重新生成新的token（也需要加）。

- jwt存储太多信息，增加了传输载荷
身份验证所需信息都被放到JWT里，如果还要进行一些数据交换，那载荷会更大，经过编码之后导致jwt非常长。

### 适用场景

- 有效期短
只希望被使用一次，比如，用户注册后发一封邮件让其激活账户，通常邮件中需要有一个链接，这个链接需要具备以下的特性：能够标识用户，该链接具有时效性（通常只允许几小时之内激活），不能被篡改以激活其他可能的账户，一次性的。这种场景就适合使用jwt。
而由于jwt具有一次性的特性。单点登录和会话管理非常不适合用jwt，如果在服务端部署额外的逻辑存储jwt的状态，那还不如使用session。基于session有很多成熟的框架可以开箱即用，但是用jwt还要自己实现逻辑。

