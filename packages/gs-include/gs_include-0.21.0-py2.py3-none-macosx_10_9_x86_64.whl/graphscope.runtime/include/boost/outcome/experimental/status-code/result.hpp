/* A partial result based on std::variant and proposed std::error
(C) 2020-2021 Niall Douglas <http://www.nedproductions.biz/> (11 commits)
File Created: Jan 2020


Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
*/

#ifndef BOOST_OUTCOME_SYSTEM_ERROR2_RESULT_HPP
#define BOOST_OUTCOME_SYSTEM_ERROR2_RESULT_HPP

#include "error.hpp"

#if __cplusplus >= 201703L || _HAS_CXX17
#if __has_include(<variant>)

#include <exception>
#include <variant>

BOOST_OUTCOME_SYSTEM_ERROR2_NAMESPACE_BEGIN

template <class T> inline constexpr std::in_place_type_t<T> in_place_type{};

template <class T> class result;

//! \brief A trait for detecting result types
template <class T> struct is_result : public std::false_type
{
};
template <class T> struct is_result<result<T>> : public std::true_type
{
};

/*! \brief Exception type representing the failure to retrieve an error.
 */
class bad_result_access : public std::exception
{
public:
  bad_result_access() = default;
  //! Return an explanatory string
  virtual const char *what() const noexcept override { return "bad result access"; }  // NOLINT
};

namespace detail
{
  struct void_
  {
  };
  template <class T> using devoid = std::conditional_t<std::is_void_v<T>, void_, T>;
}  // namespace detail

/*! \class result
\brief A imperfect `result<T>` type with its error type hardcoded to `error`, only available on C++ 17 or later.

Note that the proper `result<T>` type does not have the possibility of
valueless by exception state. This implementation is therefore imperfect.
*/
template <class T> class result : protected std::variant<BOOST_OUTCOME_SYSTEM_ERROR2_NAMESPACE::error, detail::devoid<T>>
{
  using _base = std::variant<BOOST_OUTCOME_SYSTEM_ERROR2_NAMESPACE::error, detail::devoid<T>>;
  static_assert(!std::is_reference_v<T>, "Type cannot be a reference");
  static_assert(!std::is_array_v<T>, "Type cannot be an array");
  static_assert(!std::is_same_v<T, BOOST_OUTCOME_SYSTEM_ERROR2_NAMESPACE::error>, "Type cannot be a std::error");
  // not success nor failure types

  struct _implicit_converting_constructor_tag
  {
  };
  struct _explicit_converting_constructor_tag
  {
  };
  struct _implicit_constructor_tag
  {
  };
  struct _implicit_in_place_value_constructor_tag
  {
  };
  struct _implicit_in_place_error_constructor_tag
  {
  };

public:
  //! The value type
  using value_type = T;
  //! The error type
  using error_type = BOOST_OUTCOME_SYSTEM_ERROR2_NAMESPACE::error;
  //! The value type, if it is available, else a usefully named unusable internal type
  using value_type_if_enabled = detail::devoid<T>;
  //! Used to rebind result types
  template <class U> using rebind = result<U>;

protected:
  constexpr void _check() const
  {
    if(_base::index() == 0)
    {
      std::get_if<0>(this)->throw_exception();
    }
  }
  constexpr
#ifdef _MSC_VER
  __declspec(noreturn)
#elif defined(__GNUC__) || defined(__clang__)
        __attribute__((noreturn))
#endif
  void _ub()
  {
    assert(false);  // NOLINT
#if defined(__GNUC__) || defined(__clang__)
    __builtin_unreachable();
#elif defined(_MSC_VER)
    __assume(0);
#endif
  }

public:
  constexpr _base &_internal() noexcept { return *this; }
  constexpr const _base &_internal() const noexcept { return *this; }

  //! Default constructor is disabled
  result() = delete;
  //! Copy constructor
  result(const result &) = delete;
  //! Move constructor
  result(result &&) = default;
  //! Copy assignment
  result &operator=(const result &) = delete;
  //! Move assignment
  result &operator=(result &&) = default;
  //! Destructor
  ~result() = default;

  //! Implicit result converting move constructor
  template <class U, std::enable_if_t<std::is_convertible_v<U, T>, bool> = true>
  constexpr result(result<U> &&o, _implicit_converting_constructor_tag = {}) noexcept(std::is_nothrow_constructible_v<T, U>)
      : _base(std::move(o))
  {
  }
  //! Implicit result converting copy constructor
  template <class U, std::enable_if_t<std::is_convertible_v<U, T>, bool> = true>
  constexpr result(const result<U> &o, _implicit_converting_constructor_tag = {}) noexcept(std::is_nothrow_constructible_v<T, U>)
      : _base(o)
  {
  }
  //! Explicit result converting move constructor
  template <class U, std::enable_if_t<std::is_constructible_v<T, U>, bool> = true>
  constexpr explicit result(result<U> &&o, _explicit_converting_constructor_tag = {}) noexcept(std::is_nothrow_constructible_v<T, U>)
      : _base(std::move(o))
  {
  }
  //! Explicit result converting copy constructor
  template <class U, std::enable_if_t<std::is_constructible_v<T, U>, bool> = true>
  constexpr explicit result(const result<U> &o, _explicit_converting_constructor_tag = {}) noexcept(std::is_nothrow_constructible_v<T, U>)
      : _base(o)
  {
  }

  //! Anything which `std::variant<error, T>` will construct from, we shall implicitly construct from
  using _base::_base;

  //! Special case `in_place_type_t<void>`
  constexpr explicit result(std::in_place_type_t<void> /*unused*/) noexcept
      : _base(in_place_type<detail::void_>)
  {
  }

  //! Implicit in-place converting error constructor
  template <class Arg1, class Arg2, class... Args,                                                                                                    //
            std::enable_if_t<!(std::is_constructible_v<value_type, Arg1, Arg2, Args...> && std::is_constructible_v<error_type, Arg1, Arg2, Args...>)  //
                             &&std::is_constructible_v<error_type, Arg1, Arg2, Args...>,
                             bool> = true,
            long = 5>
  constexpr result(Arg1 &&arg1, Arg2 &&arg2, Args &&... args) noexcept(std::is_nothrow_constructible_v<error_type, Arg1, Arg2, Args...>)
      : _base(std::in_place_index<0>, std::forward<Arg1>(arg1), std::forward<Arg2>(arg2), std::forward<Args>(args)...)
  {
  }

  //! Implicit in-place converting value constructor
  template <class Arg1, class Arg2, class... Args,                                                                                                    //
            std::enable_if_t<!(std::is_constructible_v<value_type, Arg1, Arg2, Args...> && std::is_constructible_v<error_type, Arg1, Arg2, Args...>)  //
                             &&std::is_constructible_v<value_type, Arg1, Arg2, Args...>,
                             bool> = true,
            int = 5>
  constexpr result(Arg1 &&arg1, Arg2 &&arg2, Args &&... args) noexcept(std::is_nothrow_constructible_v<value_type, Arg1, Arg2, Args...>)
      : _base(std::in_place_index<1>, std::forward<Arg1>(arg1), std::forward<Arg2>(arg2), std::forward<Args>(args)...)
  {
  }

  //! Implicit construction from any type where an ADL discovered `make_status_code(T, Args ...)` returns a `status_code`.
  template <class U, class... Args,                                                                            //
            class MakeStatusCodeResult = typename detail::safe_get_make_status_code_result<U, Args...>::type,  // Safe ADL lookup of make_status_code(), returns void if not found
            typename std::enable_if<!std::is_same<typename std::decay<U>::type, result>::value                 // not copy/move of self
                                    && !std::is_same<typename std::decay<U>::type, value_type>::value          // not copy/move of value type
                                    && is_status_code<MakeStatusCodeResult>::value                             // ADL makes a status code
                                    && std::is_constructible<error_type, MakeStatusCodeResult>::value,         // ADLed status code is compatible
                                    bool>::type = true>
  constexpr result(U &&v, Args &&... args) noexcept(noexcept(make_status_code(std::declval<U>(), std::declval<Args>()...)))  // NOLINT
      : _base(std::in_place_index<0>, make_status_code(static_cast<U &&>(v), static_cast<Args &&>(args)...))
  {
  }

  //! Swap with another result
  constexpr void swap(result &o) noexcept(std::is_nothrow_swappable_v<_base>) { _base::swap(o); }

  //! Clone the result
  constexpr result clone() const { return has_value() ? result(value()) : result(error().clone()); }

  //! True if result has a value
  constexpr bool has_value() const noexcept { return _base::index() == 1; }
  //! True if result has a value
  explicit operator bool() const noexcept { return has_value(); }
  //! True if result has an error
  constexpr bool has_error() const noexcept { return _base::index() == 0; }

  //! Accesses the value if one exists, else calls `.error().throw_exception()`.
  constexpr value_type_if_enabled &value() &
  {
    _check();
    return std::get<1>(*this);
  }
  //! Accesses the value if one exists, else calls `.error().throw_exception()`.
  constexpr const value_type_if_enabled &value() const &
  {
    _check();
    return std::get<1>(*this);
  }
  //! Accesses the value if one exists, else calls `.error().throw_exception()`.
  constexpr value_type_if_enabled &&value() &&
  {
    _check();
    return std::get<1>(std::move(*this));
  }
  //! Accesses the value if one exists, else calls `.error().throw_exception()`.
  constexpr const value_type_if_enabled &&value() const &&
  {
    _check();
    return std::get<1>(std::move(*this));
  }

  //! Accesses the error if one exists, else throws `bad_result_access`.
  constexpr error_type &error() &
  {
    if(!has_error())
    {
#ifndef BOOST_NO_EXCEPTIONS
      throw bad_result_access();
#else
      abort();
#endif
    }
    return *std::get_if<0>(this);
  }
  //! Accesses the error if one exists, else throws `bad_result_access`.
  constexpr const error_type &error() const &
  {
    if(!has_error())
    {
#ifndef BOOST_NO_EXCEPTIONS
      throw bad_result_access();
#else
      abort();
#endif
    }
    return *std::get_if<0>(this);
  }
  //! Accesses the error if one exists, else throws `bad_result_access`.
  constexpr error_type &&error() &&
  {
    if(!has_error())
    {
#ifndef BOOST_NO_EXCEPTIONS
      throw bad_result_access();
#else
      abort();
#endif
    }
    return std::move(*std::get_if<0>(this));
  }
  //! Accesses the error if one exists, else throws `bad_result_access`.
  constexpr const error_type &&error() const &&
  {
    if(!has_error())
    {
#ifndef BOOST_NO_EXCEPTIONS
      throw bad_result_access();
#else
      abort();
#endif
    }
    return std::move(*std::get_if<0>(this));
  }

  //! Accesses the value, being UB if none exists
  constexpr value_type_if_enabled &assume_value() & noexcept
  {
    if(!has_value())
    {
      _ub();
    }
    return *std::get_if<1>(this);
  }
  //! Accesses the error, being UB if none exists
  constexpr const value_type_if_enabled &assume_value() const &noexcept
  {
    if(!has_value())
    {
      _ub();
    }
    return *std::get_if<1>(this);
  }
  //! Accesses the error, being UB if none exists
  constexpr value_type_if_enabled &&assume_value() && noexcept
  {
    if(!has_value())
    {
      _ub();
    }
    return std::move(*std::get_if<1>(this));
  }
  //! Accesses the error, being UB if none exists
  constexpr const value_type_if_enabled &&assume_value() const &&noexcept
  {
    if(!has_value())
    {
      _ub();
    }
    return std::move(*std::get_if<1>(this));
  }

  //! Accesses the error, being UB if none exists
  constexpr error_type &assume_error() & noexcept
  {
    if(!has_error())
    {
      _ub();
    }
    return *std::get_if<0>(this);
  }
  //! Accesses the error, being UB if none exists
  constexpr const error_type &assume_error() const &noexcept
  {
    if(!has_error())
    {
      _ub();
    }
    return *std::get_if<0>(this);
  }
  //! Accesses the error, being UB if none exists
  constexpr error_type &&assume_error() && noexcept
  {
    if(!has_error())
    {
      _ub();
    }
    return std::move(*std::get_if<0>(this));
  }
  //! Accesses the error, being UB if none exists
  constexpr const error_type &&assume_error() const &&noexcept
  {
    if(!has_error())
    {
      _ub();
    }
    return std::move(*std::get_if<0>(this));
  }
};

//! True if the two results compare equal.
template <class T, class U, typename = decltype(std::declval<T>() == std::declval<U>())> constexpr inline bool operator==(const result<T> &a, const result<U> &b) noexcept
{
  const auto &x = a._internal();
  return x == b;
}
//! True if the two results compare unequal.
template <class T, class U, typename = decltype(std::declval<T>() != std::declval<U>())> constexpr inline bool operator!=(const result<T> &a, const result<U> &b) noexcept
{
  const auto &x = a._internal();
  return x != b;
}

BOOST_OUTCOME_SYSTEM_ERROR2_NAMESPACE_END

#endif
#endif
#endif
