<?php

declare(strict_types=1);

namespace Src\Users\App\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Password;
use Src\Users\Domain\DataTransferObjects\UserDto;
use Src\Users\Domain\Models\User;

class UpsertUserRequest extends FormRequest
{
    public const string NAME = 'name';

    public const string EMAIL = 'email_address';

    public const string PASSWORD = 'password';

    public const string USERNAME = 'username';

    /**
     * @return array<string, mixed>
     */
    public function rules(): array
    {
        /** @var User|null $user */
        $user = $this->route('user');

        return [
            self::NAME => ['required', 'string', 'min:4', 'max:80'],
            self::EMAIL => [
                'required',
                'max:100',
                Rule::email()
                    ->strict(),
                Rule::unique(User::class, 'email')
                    ->ignore($user?->id),
            ],
            self::PASSWORD => [
                'required',
                Password::min(8)
                    ->max(64)
                    ->letters()
                    ->numbers()
                    ->uncompromised(),
                'confirmed',
            ],
            self::USERNAME => ['required', 'string', 'max:100'],

        ];
    }

    public function toDto(): UserDto
    {
        return new UserDto(
            name: $this->string(self::NAME)->toString(),
            emailAddress: $this->string(self::EMAIL)->toString(),
            password: $this->string(self::PASSWORD)->toString(),
            username: $this->string(self::USERNAME)->toString(),
        );
    }
}
